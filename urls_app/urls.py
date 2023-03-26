from django.urls import path
from urls_app.views import CreateShortURLView

urlpatterns = [
    path("", CreateShortURLView.as_view(), name="create-short-url"),
]
