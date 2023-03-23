import environ

from .handler import env
from .path import BASE_DIR

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users_app.UserModel"

POSTGRES_HOST = env.str("POSTGRES_HOST", None)

if POSTGRES_HOST is None:
    postgres_env_file_path = BASE_DIR / "deploy" / "envs" / "postgres.env"
    try:
        environ.Env.read_env(postgres_env_file_path)
    except:
        raise ImportError(
            f"Cannot read local `{str(postgres_env_file_path.resolve())}` file "
            f"to parse environment variables in local runtime"
        )

    POSTGRES_HOST = env.str("POSTGRES_HOST")

POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_PORT = env.int("POSTGRES_PORT")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}
