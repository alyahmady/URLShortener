import datetime

from bson import ObjectId
from bson.errors import BSONError
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import InvalidParameterException
from URLShortener.utils import jsonable_encoder
from urls_app.models import URLCollection
from urls_app.services import generate_url_slug


class CreateShortURLSerializer(serializers.Serializer):
    original_url = serializers.URLField(required=True, max_length=2000)

    lifespan_hours = serializers.IntegerField(
        required=False, min_value=1, max_value=settings.URL_LIFESPAN_HOURS
    )

    def save(self, user_id: str | ObjectId):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
        except (LookupError, BSONError, TypeError) as exc:
            raise InvalidParameterException(ErrorCode.INVALID_USER_ID) from exc

        now = timezone.now()
        expire_date_time = now + datetime.timedelta(hours=settings.URL_LIFESPAN_HOURS)

        if "lifespan_hours" in self.validated_data:
            lifespan_hours = self.validated_data.pop("lifespan_hours")
            if lifespan_hours <= settings.URL_LIFESPAN_HOURS:
                expire_date_time = now + datetime.timedelta(hours=lifespan_hours)

        url_validated_data = self.validated_data | {
            "created_at": now,
            "expire_at": expire_date_time,
            "user_id": user_id,
        }

        url_id, url_slug = generate_url_slug(max_retry=5)
        URLCollection.update_one(
            filter={"_id": url_id}, update={"$set": url_validated_data}, upsert=False
        )

        url_object: dict = URLCollection.find_one({"_id": url_id})
        url_object = jsonable_encoder(url_object)

        cache.set(
            key=settings.URL_CACHE_KEY.format(slug=url_slug),
            value=settings.URL_CACHE_VALUE.format(
                hit=0, original_url=url_validated_data["original_url"]
            ),
            timeout=settings.URL_CACHE_MIN_TTL_SECONDS,
        )

        return url_object
