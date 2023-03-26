from .handler import env

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("auth_app.services.CustomJWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "URLShortener.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "600/day",
        "user": "650/day",
        "token_obtain": "25/day",
        "token_refresh": "1/day",
        "create_short_url": "100/day",
        "short_url_redirect": "500/day",
        "user_register": "5/day",
        "healthcheck": "1000/day",
    },
}

API_VERSION = env.int("API_VERSION", 1)
API_PREFIX = env.str("API_PREFIX", f"api/v") + f"{API_VERSION}"
