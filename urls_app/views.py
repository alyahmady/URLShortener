from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import NotFoundEntityException
from URLShortener.permissions import IsAuthenticated
from URLShortener.responses import SuccessResponse, ErrorResponse
from URLShortener.serializers import ResponseSerializer
from auth_app.services import CustomJWTAuthentication
from urls_app.models import URLCollection
from urls_app.serializers import CreateShortURLSerializer


class CreateShortURLView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    throttle_scope = "create_short_url"

    @extend_schema(
        description="Creating a short URL which will be redirected to the `original_url`",
        methods=["POST"],
        request=CreateShortURLSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ResponseSerializer, description="Successfully created"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ResponseSerializer, description="Bad payload"
            ),
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=ResponseSerializer, description="Database is down"
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=ResponseSerializer, description="Access denied. Too many requests"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ResponseSerializer,
                description="Failed in unique URL slug generation",
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
                response=ResponseSerializer, description="Email taken (duplicate user)"
            ),
        },
    )
    def post(self, request: Request, **kwargs):
        serializer = CreateShortURLSerializer(data=request.data)
        if serializer.is_valid():
            url_object = serializer.save(user_id=request.user["_id"])
            return SuccessResponse(
                message="Short URL created successfully.",
                data=url_object,
                status_code=status.HTTP_201_CREATED,
            )

        return ErrorResponse(
            message="Failed in creating URL",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class RedirectShortURLView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "short_url_redirect"

    @extend_schema(
        description="Redirecting a short URL (with slug) to the `original_url`",
        methods=["GET"],
        request=CreateShortURLSerializer,
        responses={
            status.HTTP_301_MOVED_PERMANENTLY: OpenApiResponse(
                description="Successfully redirected"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ResponseSerializer, description="Bad payload"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ResponseSerializer, description="URL Slug not found"
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=ResponseSerializer, description="Access denied. Too many requests"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ResponseSerializer,
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
                response=ResponseSerializer, description="Database is temporarily down"
            ),
        },
    )
    def get(self, request: Request, **kwargs):
        url_slug = self.kwargs["url_slug"]

        cached_original_url = cache.get(
            key=settings.URL_CACHE_KEY.format(slug=url_slug),
        )

        if cached_original_url:
            # Get cached value
            hit, *original_url = cached_original_url.split(";")
            original_url = "".join(original_url)

            # Increase hit count and time-to-live of Redis key (20-80 Rule)
            hit = int(hit) + 1

            ttl = settings.URL_CACHE_MIN_TTL_SECONDS * hit
            ttl = min(ttl, settings.URL_CACHE_MAX_TTL_SECONDS)

            cache.set(
                key=settings.URL_CACHE_KEY.format(slug=url_slug),
                value=settings.URL_CACHE_VALUE.format(
                    hit=hit, original_url=original_url
                ),
                timeout=ttl,
            )

        else:
            url_object = URLCollection.find_one(
                filter={"slug": url_slug}, projection={"original_url": True}
            )
            if not url_object:
                raise NotFoundEntityException(ErrorCode.SHORT_URL_NOT_FOUND)

            original_url = url_object["original_url"]

            cache.set(
                key=settings.URL_CACHE_KEY.format(slug=url_slug),
                value=settings.URL_CACHE_VALUE.format(hit=0, original_url=original_url),
                timeout=settings.URL_CACHE_MIN_TTL_SECONDS,
            )

        return HttpResponseRedirect(
            redirect_to=original_url, status=status.HTTP_301_MOVED_PERMANENTLY
        )
