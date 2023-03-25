from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Swagger
    path(f"{settings.API_PREFIX}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{settings.API_PREFIX}/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "{settings.API_PREFIX}/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # API Routes
    path("{settings.API_PREFIX}/auth/", include("auth_app.urls")),
]

urlpatterns += [
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
