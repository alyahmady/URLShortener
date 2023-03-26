from bson import ObjectId
from bson.errors import BSONError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from URLShortener.error_codes import ErrorCode
from users_app.models import UserCollection


class CustomJWTAuthentication(JWTAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def is_user_active(self, user: dict, raise_exc: bool = True):
        is_active = user.get("is_active")
        if not is_active:
            if raise_exc:
                raise AuthenticationFailed(code=ErrorCode.INACTIVE_USER)
            return False

        return True

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """

        try:
            return AccessToken(raw_token)
        except TokenError as exc:
            raise AuthenticationFailed(code=ErrorCode.INVALID_TOKEN) from exc

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token["user_id"]
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
        except (LookupError, BSONError, TypeError) as exc:
            raise AuthenticationFailed(code=ErrorCode.INVALID_TOKEN) from exc

        user = UserCollection.find_one(filter={"_id": user_id})
        if not user:
            raise AuthenticationFailed(code=ErrorCode.USER_NOT_FOUND)

        if self.is_user_active(user, raise_exc=True):
            return user
