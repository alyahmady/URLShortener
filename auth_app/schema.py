from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from auth_app.services import CustomJWTAuthentication


class CustomJWTAuthenticationScheme(SimpleJWTScheme):
    name = "Custom JWT Auth"
    target_class = CustomJWTAuthentication
