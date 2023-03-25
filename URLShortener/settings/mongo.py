import environ
import pymongo

from .handler import env
from .path import BASE_DIR

MONGODB_HOST = env.str("MONGODB_HOST", None)

if MONGODB_HOST is None:
    mongodb_env_file_path = BASE_DIR / "deploy" / "envs" / "mongodb.env"
    try:
        environ.Env.read_env(mongodb_env_file_path)
    except:
        raise ImportError(
            f"Cannot read local `{str(mongodb_env_file_path.resolve())}` file "
            f"to parse environment variables in local runtime"
        )

    MONGODB_HOST = env.str("MONGODB_HOST")


MONGODB_PORT = env.int("MONGODB_PORT")

MONGODB_USERNAME = env.str("MONGODB_USERNAME", None)
MONGODB_PASSWORD = env.str("MONGODB_PASSWORD", None)

MONGODB_TLS = env.bool("MONGODB_TLS")

MONGODB_CONNECTION_TIMEOUT_SECONDS = env.int("MONGODB_CONNECTION_TIMEOUT_SECONDS", 20)
MONGODB_MIN_CONNECTION_POOL_SIZE = env.int("MONGODB_MIN_CONNECTION_POOL_SIZE", 1)
MONGODB_MAX_CONNECTION_POOL_SIZE = env.int("MONGODB_MAX_CONNECTION_POOL_SIZE", 100)

MONGODB_DB_NAME = env.str("MONGODB_DB_NAME")

MONGODB_USERS_COLLECTION_NAME = env.str("MONGODB_USERS_COLLECTION_NAME", "auth_users")
MONGODB_URLS_COLLECTION_NAME = env.str("MONGODB_URLS_COLLECTION_NAME", "shortened_urls")

# Values are unique indexes of that collection
MONGODB_COLLECTIONS = {
    MONGODB_USERS_COLLECTION_NAME: [
        ("email", pymongo.ASCENDING),
    ],
    MONGODB_URLS_COLLECTION_NAME: [
        ("slug", pymongo.DESCENDING),
    ],
}
