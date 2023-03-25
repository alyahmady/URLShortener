from bson import ObjectId
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import (
    InternalAuthException,
    BaseCustomException,
    AuthException,
)
from users_app.models import UserCollection


class CustomAuthBackend(BaseBackend):
    def is_user_active(self, user: dict, raise_exc: bool = True):
        is_active = user.get("is_active")
        if not is_active:
            if raise_exc:
                raise AuthException(ErrorCode.INACTIVE_USER)
            return False

        return True

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return

        user = UserCollection.find_one({"email": email})

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

        if self.is_user_active(user, raise_exc=True):
            return user

    def get_user(self, user_id: str | ObjectId) -> dict:
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        user: dict = UserCollection.find_one({"_id": user_id})

        if self.is_user_active(user, raise_exc=True):
            return user
