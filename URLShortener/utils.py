import re
import string

from bson import ObjectId
from django.conf import settings

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import InvalidDataException


def jsonable_encoder(data: dict, printable: bool = True) -> dict:
    id_keys = (("_id", "id"), ("user_id", "user_id"))
    for key, printable_key in id_keys:
        if key in data:
            id_value = data.pop(key)
            if isinstance(id_value, ObjectId):
                id_value = str(id_value)

            id_key = printable_key if printable is True else key
            data = {id_key: id_value} | data

    return data


def validate_password_string(password: str, raise_exc: bool = True) -> bool:
    try:
        if len(password) < settings.USER_PASSWORD_MIN_LEN:
            raise InvalidDataException(
                code=ErrorCode.INVALID_PASSWORD,
                extra_message=f"Its length must be at least {settings.USER_PASSWORD_MIN_LEN}.",
            )

        if settings.USER_PASSWORD_UPPER_AND_LOWER_REQUIRED is True:
            if password == password.lower() or password == password.upper():
                raise InvalidDataException(
                    code=ErrorCode.INVALID_PASSWORD,
                    extra_message="It must contain both uppercase and lowercase letters.",
                )

        if settings.USER_PASSWORD_NUMERIC_REQUIRED is True:
            if not bool(re.search(r"\d", password)):
                raise InvalidDataException(
                    code=ErrorCode.INVALID_PASSWORD,
                    extra_message="It must contain digits.",
                )

        if settings.USER_PASSWORD_SPECIAL_CHAR_REQUIRED is True:
            if not any(char in set(string.punctuation) for char in password):
                raise InvalidDataException(
                    code=ErrorCode.INVALID_PASSWORD,
                    extra_message="It must contain special characters.",
                )

    except InvalidDataException as exc:
        if raise_exc is True:
            raise exc
        return False

    else:
        return True
