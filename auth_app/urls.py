from django.urls import path

from auth_app.views import CustomTokenObtainPairView, CustomTokenRefreshView

app_name = "auth_app"

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("login/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
]
