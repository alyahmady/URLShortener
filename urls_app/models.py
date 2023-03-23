from django.db import models


class URLModel(models.Model):
    # Identifier
    identifier = models.CharField(max_length=20, primary_key=True, db_index=True)

    # Relations
    user = models.ForeignKey(
        "users_app.UserModel",
        on_delete=models.CASCADE,
        related_name="urls",
        null=False,
        blank=False,
    )

    # URLs
    original_url = models.URLField(max_length=2000, null=False, blank=False)

    # Date time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return ""

    class Meta:
        app_label = "urls_app"
        db_table = "shortened_urls"
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"
        ordering = ("-created_at",)
