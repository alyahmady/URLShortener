import traceback
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response as DRFResponse
from rest_framework.views import exception_handler

from URLShortener.error_codes import ErrorCode
from URLShortener.logging import debug_logger, error_logger
from URLShortener.responses import ErrorResponse


def custom_exception_handler(exc: Exception, context: dict):
    if isinstance(exc, BaseCustomException):
        headers = {}
        if exc.auth_header:
            headers["WWW-Authenticate"] = exc.auth_header
        if exc.wait and exc.wait.isdigit():
            headers["Retry-After"] = str(exc.wait)

        return ErrorResponse(
            message=exc.message,
            data=exc.data,
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

    debug_logger.exception(f"ID: {error_id} - Data: {response.data}")
    return ErrorResponse(
        message="Unknown error",
        data={"error_id": error_id},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class BaseCustomException(Exception):
    def __init__(self, code: ErrorCode):
        self.auth_header = ""
        self.wait = ""

        self.message = code.value["message"]
        self.code = code.value["code"]
        self.status = code.value["status"]
        self.data = code.value.get("data")


class CustomInternalException(BaseCustomException):
    def __init__(self, code: ErrorCode):
        super().__init__(code)

        debug_logger.exception(
            f"Message: {self.message} \n"
            f"Code: {self.code} \n"
            f"Status: {self.status}"
        )


class CustomResponseException(BaseCustomException):
    ...


class ConnectionException(CustomInternalException):
    ...


class InvalidParameterException(CustomInternalException):
    ...


class InternalAuthException(CustomInternalException):
    ...


class AuthException(BaseCustomException):
    ...
