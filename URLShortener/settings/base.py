import environ

from .handler import env
from .path import BASE_DIR

# Important
DEBUG = env.bool("DEBUG", None)

if DEBUG is None:
    django_env_file_path = BASE_DIR / "deploy" / "envs" / "django.env"
    try:
        environ.Env.read_env(django_env_file_path)
    except:
        raise ImportError(
            f"Cannot read local `{str(django_env_file_path.resolve())}` file "
            f"to parse environment variables in local runtime"
        )

    DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env.str("SECRET_KEY")

# Django main routes
WSGI_APPLICATION = "URLShortener.wsgi.application"

ROOT_URLCONF = "URLShortener.urls"

# Security checks
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Others
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



