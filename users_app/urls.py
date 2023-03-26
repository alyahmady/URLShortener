from django.urls import path

from users_app.views import UserRegisterView

app_name = "users_app"

urlpatterns = [
    path("", UserRegisterView.as_view(), name="user-register"),
]
