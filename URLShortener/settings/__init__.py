from .apps import INSTALLED_APPS
from .base import (
    ALLOWED_HOSTS,
    WSGI_APPLICATION,
    MIDDLEWARE,
    SECRET_KEY,
    ROOT_URLCONF,
    DEBUG,
    TEMPLATES,
    CSRF_TRUSTED_ORIGINS,
)
from .cache import (
    CACHES,
    REDIS_PASSWORD,
    REDIS_USER,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_CONNECTION_URI,
    CACHE_VERSION,
)
from .cors import CORS_ALLOWED_ORIGINS, CORS_ALLOW_ALL_ORIGINS
from .jwt import SIMPLE_JWT
from .logging import LOGS_DIR, CORE_LOG_FILE, ERROR_LOG_FILE, DEBUG_LOG_FILE
from .misc import LANGUAGE_CODE, USE_TZ, USE_I18N, TIME_ZONE
from .mongo import (
    MONGODB_COLLECTIONS,
    MONGODB_URLS_COLLECTION_NAME,
    MONGODB_USERS_COLLECTION_NAME,
    MONGODB_PASSWORD,
    MONGODB_USERNAME,
    MONGODB_TLS,
    MONGODB_PORT,
    MONGODB_HOST,
    MONGODB_DB_NAME,
    MONGODB_CONNECTION_TIMEOUT_SECONDS,
    MONGODB_MAX_CONNECTION_POOL_SIZE,
    MONGODB_MIN_CONNECTION_POOL_SIZE,
)
from .password import (
    AUTH_PASSWORD_VALIDATORS,
    USER_PASSWORD_MIN_LEN,
    USER_PASSWORD_NUMERIC_REQUIRED,
    USER_PASSWORD_UPPER_AND_LOWER_REQUIRED,
    USER_PASSWORD_SPECIAL_CHAR_REQUIRED,
)
from .path import (
    BASE_DIR,
    STATIC_URL,
    STATIC_ROOT,
    STATICFILES_DIRS,
    STATICFILES_FINDERS,
    MEDIA_URL,
    MEDIA_ROOT,
)
from .rest_framework import API_PREFIX, API_VERSION, REST_FRAMEWORK
from .swagger import SPECTACULAR_SETTINGS
from .url import URL_LIFESPAN_HOURS
