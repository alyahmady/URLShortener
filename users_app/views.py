from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from URLShortener.responses import SuccessResponse, ErrorResponse
from URLShortener.serializers import ResponseSerializer
from users_app.serializers import (
    UserRegisterSerializer,
)


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "user_register"

    @extend_schema(
        description="Registering a new user",
        methods=["POST"],
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ResponseSerializer, description="Successfully registered"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ResponseSerializer, description="Bad payload"
            ),
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=ResponseSerializer, description="Email taken (duplicate user)"
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                response=ResponseSerializer, description="Access denied. Too many requests"
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
                response=ResponseSerializer, description="Database is down"
            ),
        },
    )
    def post(self, request, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_object = serializer.save()
            return SuccessResponse(
                message="User registered successfully.",
                data=user_object,
                status_code=status.HTTP_201_CREATED,
            )

        return ErrorResponse(
            message="Failed in registering user",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
