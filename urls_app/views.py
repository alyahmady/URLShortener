from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView

from URLShortener.permissions import IsAuthenticated
from URLShortener.responses import SuccessResponse, ErrorResponse
from URLShortener.serializers import ResponseSerializer
from auth_app.services import CustomJWTAuthentication
from urls_app.serializers import CreateShortURLSerializer


class CreateShortURLView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

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
