import mimetypes
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Related to issue on parsing static files of admin panel in localhost with Chrome
mimetypes.add_type("application/javascript", ".js", True)

# MEDIA
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
