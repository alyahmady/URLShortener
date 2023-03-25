from .handler import env

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("auth_app.services.CustomJWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "URLShortener.exceptions.custom_exception_handler",
}

API_VERSION = env.int("API_VERSION", 1)
API_PREFIX = env.str("API_PREFIX", f"api/v") + f"{API_VERSION}"
