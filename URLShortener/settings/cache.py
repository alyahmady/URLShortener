import environ

from .handler import env
from .path import BASE_DIR

REDIS_HOST = env.str("REDIS_HOST", None)

if REDIS_HOST is None:
    redis_env_file_path = BASE_DIR / "deploy" / "envs" / "redis.env"
    try:
        environ.Env.read_env(redis_env_file_path)
    except:
        raise ImportError(
            f"Cannot read local `{str(redis_env_file_path.resolve())}` file "
            f"to parse environment variables in local runtime"
        )

    REDIS_HOST = env.str("REDIS_HOST")

REDIS_USER = env.str("REDIS_USER", "default")
REDIS_PORT = env.str("REDIS_PORT_NUMBER", "6379")
REDIS_CONNECTION_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CACHE_VERSION = env.int("CACHE_VERSION", 1)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONNECTION_URI,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,
        },
        "KEY_PREFIX": "URLSHORTENER",
        "VERSION": CACHE_VERSION,
    }
}

REDIS_PASSWORD = env.str("REDIS_PASSWORD", None)
if REDIS_PASSWORD:
    CACHES["default"]["OPTIONS"]["PASSWORD"] = REDIS_PASSWORD
    REDIS_CONNECTION_URI = (
        f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    )
    CACHES["default"]["LOCATION"] = REDIS_CONNECTION_URI
