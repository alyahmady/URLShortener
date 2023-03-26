from .handler import env

# For User Registration
USER_PASSWORD_MIN_LEN = env.int("USER_PASSWORD_MIN_LEN", 8)
USER_PASSWORD_UPPER_AND_LOWER_REQUIRED = env.bool(
    "USER_PASSWORD_UPPER_AND_LOWER_REQUIRED", True
)
USER_PASSWORD_NUMERIC_REQUIRED = env.bool("USER_PASSWORD_NUMERIC_REQUIRED", True)
USER_PASSWORD_SPECIAL_CHAR_REQUIRED = env.bool(
    "USER_PASSWORD_SPECIAL_CHAR_REQUIRED", True
)

# For Django usage
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
