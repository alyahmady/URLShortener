DEFAULT_INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DJANGO_INSTALLED_APPS = [
    "users_app.apps.UsersAppConfig",
    "urls_app.apps.UrlsAppConfig",
    "auth_app.apps.AuthAppConfig",
]

THIRD_PARTY_INSTALLED_APPS = []

INSTALLED_APPS = (
    DEFAULT_INSTALLED_APPS + DJANGO_INSTALLED_APPS + THIRD_PARTY_INSTALLED_APPS
)
