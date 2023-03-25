from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, message=None, data=None, code=2000, status_code=status.HTTP_200_OK, *args, **kwargs):

        # Filtering kwargs
        extra_kwargs = kwargs
        response_kwargs = (
            "data",
            "status",
            "template_name",
            "headers",
            "exception",
            "content_type",
        )
        kwargs = {
            key: value for key, value in extra_kwargs.items() if key in response_kwargs
        }
        super().__init__(status=status_code, data=data, **kwargs)

        self.message = message
        self.status_code = status_code

        self.data = OrderedDict(
            {
                "status": self.status_code,
                "message": message,
                "result": data,
            }
        )

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.data


class SuccessResponse(CustomResponse):
    def __init__(
        self, message=None, data=None, status_code=status.HTTP_200_OK, *args, **kwargs
    ):
        super().__init__(message, data, status_code, *args, **kwargs)


class ErrorResponse(CustomResponse):
    def __init__(
        self,
        message=None,
        data=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs
    ):
        super().__init__(message, data, status_code, *args, **kwargs)
