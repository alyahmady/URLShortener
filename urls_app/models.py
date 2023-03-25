from django.conf import settings

from URLShortener.mongo import MongoDB

URLCollection = MongoDB.get_collection(settings.MONGODB_URLS_COLLECTION_NAME)
