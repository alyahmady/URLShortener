from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import AuthException
from auth_app.backends import CustomAuthBackend
from auth_app.token import CustomToken


class CustomTokenObtainSerializer(serializers.Serializer):
    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

        self.fields["email"] = serializers.EmailField(max_length=320)
        self.fields["password"] = PasswordField(max_length=100)

    def validate(self, data):
        self.user: dict | None = CustomAuthBackend.authenticate(
            email=data["email"], password=data["password"]
        )
        if not self.user:
            raise AuthException(ErrorCode.EMAIL_PASS_AUTH_FAILED)

        refresh = self.get_token(self.user)

        validated_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return validated_data

    @classmethod
    def get_token(cls, user: dict):
        return CustomToken.for_user(user=user)


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    def validate(self, data):
        refresh = CustomToken(data["refresh"])

        validated_data = {"access": str(refresh.access_token)}

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        validated_data["refresh"] = str(refresh)

        return validated_data
