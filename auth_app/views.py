from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from URLShortener.responses import SuccessResponse
from URLShortener.serializers import ResponseSerializer
from auth_app.serializers import (
    CustomTokenObtainSerializer,
    CustomTokenRefreshSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "token_obtain"

    @extend_schema(
        description="Takes a set of user credentials and returns an access and "
        "refresh JSON web token pair to prove the authentication of those credentials.",
        methods=["POST"],
        request=CustomTokenObtainSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ResponseSerializer, description="Successfully obtained"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ResponseSerializer, description="Bad payload"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ResponseSerializer, description="Failed in auth"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ResponseSerializer, description="Access denied"
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=ResponseSerializer,
                description="Access denied. Too many requests",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ResponseSerializer,
                description="Failed",
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
                response=ResponseSerializer, description="Database is down"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return SuccessResponse(
            message="Successful authentication",
            data=response.data,
            status_code=response.status_code,
        )


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "token_refresh"

    @extend_schema(
        description="Takes a refresh type JSON web token and returns an "
        "access type JSON web token if the refresh token is valid.",
        methods=["POST"],
        request=CustomTokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ResponseSerializer, description="Successfully obtained"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ResponseSerializer, description="Bad payload"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ResponseSerializer, description="Failed in auth"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ResponseSerializer, description="Access denied"
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=ResponseSerializer,
                description="Access denied. Too many requests",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ResponseSerializer,
                description="Failed",
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
                response=ResponseSerializer, description="Database is down"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return SuccessResponse(
            message="Successful refresh token obtained",
            data=response.data,
            status_code=response.status_code,
        )
