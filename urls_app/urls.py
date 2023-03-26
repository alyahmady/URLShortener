from django.urls import path

from urls_app.views import CreateShortURLView

app_name = "users_app"


urlpatterns = [
    path("", CreateShortURLView.as_view(), name="create-short-url"),
]
