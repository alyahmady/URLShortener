import enum

from rest_framework import status


class ErrorCode(enum.Enum):
    # Internal
    DATABASE_DOWN = {
        "message": "Database is temporary down.",
        "code": 1001,
        "status": status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    INVALID_COLLECTION = {
        "message": "Invalid database collection name.",
        "code": 1002,
        "status": status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    INTERNAL_AUTH = {
        "message": "Failed in authenticating user.",
        "code": 1003,
        "status": status.HTTP_401_UNAUTHORIZED,
    }
    INVALID_USER_ID = {
        "message": "User ID is not valid.",
        "code": 1004,
        "status": status.HTTP_400_BAD_REQUEST,
    }

    # Response
    NO_PASSWORD_FOR_USER = {
        "message": "User has no password.",
        "code": 2001,
        "status": status.HTTP_401_UNAUTHORIZED,
    }
    INACTIVE_USER = {
        "message": "User is not active.",
        "code": 2002,
        "status": status.HTTP_403_FORBIDDEN,
    }
    EMAIL_PASS_AUTH_FAILED = {
        "message": "Email or password is not correct.",
        "code": 2003,
        "status": status.HTTP_403_FORBIDDEN,
    }
    USER_NOT_FOUND = {
        "message": "User not found.",
        "code": 2004,
        "status": status.HTTP_404_NOT_FOUND,
    }
    INVALID_TOKEN = {
        "message": "Token is invalid. Authentication failed.",
        "code": 2005,
        "status": status.HTTP_401_UNAUTHORIZED,
    }
    PASSWORD_NOT_MATCH = {
        "message": "Password fields didn't match.",
        "code": 2006,
        "status": status.HTTP_400_BAD_REQUEST,
    }
    DUPLICATE_USER = {
        "message": "User email is already taken.",
        "code": 2007,
        "status": status.HTTP_409_CONFLICT,
    }
