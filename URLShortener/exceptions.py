from URLShortener.error_codes import ErrorCode
from URLShortener.logging import debug_logger


class BaseCustomException(Exception):
    def __init__(self, code: ErrorCode):
        self.message = code.value["message"]
        self.code = code.value["code"]
        self.status = code.value["status"]


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
