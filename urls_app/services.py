import secrets
from typing import Tuple

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import CustomInternalException
from urls_app.models import URLCollection


def generate_url_slug(max_retry: int = 5) -> Tuple[ObjectId, str]:
    retry_count = 0
    while True:
        if retry_count >= max_retry:
            # IMPORTANT -> critical issue, if code reach here -> Should send an email or notification to Admins
            raise CustomInternalException(ErrorCode.URL_UNIQUE_SLUG_GENERATION)

        url_slug = secrets.token_urlsafe(6).replace("_", "").replace("-", "")

        try:
            url_db_object: InsertOneResult = URLCollection.insert_one(
                {"slug": url_slug}
            )
        except DuplicateKeyError:
            retry_count += 1
            continue
        else:
            url_id = url_db_object.inserted_id
            if not isinstance(url_id, ObjectId):
                url_id = ObjectId(url_id)

            return url_id, url_slug
