# Generated by Django 4.1.7 on 2023-03-23 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="URLModel",
            fields=[
                (
                    "identifier",
                    models.CharField(
                        db_index=True, max_length=20, primary_key=True, serialize=False
                    ),
                ),
                ("original_url", models.URLField(max_length=2000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Shortened URL",
                "verbose_name_plural": "Shortened URLs",
                "db_table": "shortened_urls",
                "ordering": ("-created_at",),
            },
        ),
    ]
