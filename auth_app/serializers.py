from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import AuthException
from auth_app.token import CustomToken


class CustomTokenObtainSerializer(serializers.Serializer):
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"] = serializers.EmailField(max_length=320)
        self.fields["password"] = PasswordField(max_length=100)

    def validate(self, data):
        authenticate_kwargs = {"email": data["email"], "password": data["password"]}
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user: dict | None = authenticate(**authenticate_kwargs)
        if not self.user:
            raise AuthException(ErrorCode.EMAIL_PASS_AUTH_FAILED)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

    @classmethod
    def get_token(cls, user: dict):
        return CustomToken.for_user(user=user)


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = CustomToken

    def validate(self, data):
        refresh = self.token_class(data["refresh"])

        validated_data = {"access": str(refresh.access_token)}

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        validated_data["refresh"] = str(refresh)

        return validated_data
