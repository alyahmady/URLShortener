from django.conf import settings

from URLShortener.mongo import MongoDB

UserCollection = MongoDB.get_collection(settings.MONGODB_USERS_COLLECTION_NAME)