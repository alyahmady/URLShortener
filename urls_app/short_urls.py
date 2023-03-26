from django.urls import path

from urls_app.views import RedirectShortURLView

urlpatterns = [
    path("<str:url_slug>", RedirectShortURLView.as_view(), name="redirect-short-url"),
]
