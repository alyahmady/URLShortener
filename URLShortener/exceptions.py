import traceback
import uuid
from enum import Enum

from django.conf import settings
from pymongo.errors import PyMongoError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response as DRFResponse
from rest_framework.views import exception_handler

from URLShortener.error_codes import ErrorCode
from URLShortener.logging import debug_logger, error_logger
from URLShortener.responses import ErrorResponse


def custom_exception_handler(exc: Exception, context: dict):
    try:
        if isinstance(exc, PyMongoError):
            raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc
    except BaseCustomException as e:
        exc = e
    except:
        pass

    try:
        if isinstance(exc, AuthenticationFailed):
            if isinstance(exc.detail.code, ErrorCode):
                raise AuthException(exc.detail.code)
    except BaseCustomException as e:
        exc = e
    except:
        pass

    if isinstance(exc, BaseCustomException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = getattr(exc, "auth_header", None)
        if getattr(exc, "wait", "").isdigit():
            headers["Retry-After"] = getattr(exc, "wait", None)

        return ErrorResponse(
            message=exc.message,
            data=exc.data,
            code=exc.code,
            status_code=exc.status,
            headers=headers,
        )

    response = exception_handler(exc, context)
    error_id = uuid.uuid4()

    if isinstance(response, DRFResponse):
        if settings.DEBUG is True:
            if isinstance(response.data, dict):
                response.data.update({"debug_traceback": traceback.format_exc()})
            elif isinstance(response.data, list):
                response.data.append({"debug_traceback": traceback.format_exc()})

        error_logger.error(
            f"ID: {error_id} - Data: {response.data} - Exception: {exc.__class__.__name__} - Message: {str(exc)}"
        )
        return ErrorResponse(
            message="Error",
            data={"data": response.data, "error_id": error_id},
            status_code=response.status_code,
            headers=response.headers,
        )

    debug_logger.exception(f"ID: {error_id} - Data: {getattr(response, 'data', None)}")
    return ErrorResponse(
        message="Unknown error",
        data={"error_id": error_id},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class BaseCustomException(Exception):
    def __init__(self, code: ErrorCode | dict):
        if isinstance(code, Enum):
            code = code.value

        self.message = code["message"]
        self.code = code["code"]
        self.status = code["status"]
        self.data = code.get("data")


class CustomInternalException(BaseCustomException):
    def __init__(self, code: ErrorCode):
        super().__init__(code)

        debug_logger.exception(
            f"Message: {self.message} \n"
            f"Code: {self.code} \n"
            f"Status: {self.status}"
        )


class CustomResponseException(BaseCustomException):
    def __init__(self, code: ErrorCode, extra_message: str | None = None):
        super().__init__(code)

        if extra_message:
            self.message += f" {extra_message}"


class ConnectionException(CustomInternalException):
    ...


class InvalidParameterException(CustomInternalException):
    ...


class InternalAuthException(CustomInternalException):
    ...


class AuthException(CustomResponseException):
    ...


class InvalidDataException(CustomResponseException):
    ...


class DuplicateEntityException(CustomResponseException):
    ...
