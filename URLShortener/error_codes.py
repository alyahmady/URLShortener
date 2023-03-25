import enum

from rest_framework import status


class ErrorCode(enum.Enum):
    DATABASE_DOWN = {
        "message": "Database is temporary down.",
        "code": 1000,
        "status": status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    INVALID_COLLECTION = {
        "message": "Invalid database collection name.",
        "code": 1001,
        "status": status.HTTP_503_SERVICE_UNAVAILABLE,
    }
