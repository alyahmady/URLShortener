from bson import ObjectId
from bson.errors import BSONError
from django.contrib.auth.hashers import check_password

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import (
    InternalAuthException,
    BaseCustomException,
    AuthException,
    InvalidParameterException,
)
from users_app.models import UserCollection


class CustomAuthBackend:
    @classmethod
    def is_user_active(cls, user: dict, raise_exc: bool = True):
        is_active = user.get("is_active")
        if not is_active:
            if raise_exc:
                raise AuthException(ErrorCode.INACTIVE_USER)
            return False

        return True

    @classmethod
    def authenticate(cls, email, password):
        user = UserCollection.find_one({"email": email})
        if not user:
            return None

        try:
            hashed_password = user["hashed_password"]
            if not hashed_password:
                raise AuthException(ErrorCode.NO_PASSWORD_FOR_USER)

            assert check_password(password, hashed_password) is True

        except (LookupError, AssertionError):
            return None
        except BaseCustomException as exc:
            raise exc
        except Exception as exc:
            raise InternalAuthException(ErrorCode.INTERNAL_AUTH) from exc

        if cls.is_user_active(user, raise_exc=True):
            return user

    @classmethod
    def get_user(cls, user_id: str | ObjectId) -> dict:
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
        except (BSONError, TypeError) as exc:
            raise InvalidParameterException(ErrorCode.INVALID_USER_ID) from exc

        user: dict = UserCollection.find_one({"_id": user_id})
        if not user:
            return None

        if cls.is_user_active(user, raise_exc=True):
            return user
