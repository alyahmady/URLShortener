from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from URLShortener.views import Healthcheck

urlpatterns = [
    re_path(
        route=r"^media/(?P<path>.*)$",
        view=serve,
        kwargs={
            "document_root": settings.MEDIA_ROOT,
        },
    ),
    re_path(
        route=r"^static/(?P<path>.*)$",
        view=serve,
        kwargs={
            "document_root": settings.STATIC_ROOT,
        },
    ),
]

urlpatterns += [
    # Swagger
    path(f"{settings.API_PREFIX}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{settings.API_PREFIX}/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{settings.API_PREFIX}/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # API Routes
    path(f"{settings.API_PREFIX}/auth/", include("auth_app.urls")),
    path(f"{settings.API_PREFIX}/user/", include("users_app.urls")),
    path(f"{settings.API_PREFIX}/url/", include("urls_app.urls")),
    path(f"health-check", Healthcheck.as_view(), name="health-check"),
    path(f"", include("urls_app.short_urls")),
]
