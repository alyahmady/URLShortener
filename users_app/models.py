import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Info
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)

    # Identifier
    email = models.EmailField(unique=True, max_length=255)

    # Date time
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Flags
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = None

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}"

    class Meta:
        app_label = "users_app"
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-date_joined",)
