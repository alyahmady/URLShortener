from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from URLShortener.responses import SuccessResponse
from auth_app.serializers import (
    CustomTokenObtainSerializer,
    CustomTokenRefreshSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

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

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return SuccessResponse(
            message="Successful refresh token obtained",
            data=response.data,
            status_code=response.status_code,
        )
