from .handler import env

LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en-us")

TIME_ZONE = env.str("TIME_ZONE", "UTC")

USE_I18N = True

USE_TZ = True
