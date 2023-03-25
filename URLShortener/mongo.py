from django.conf import settings
from pymongo import MongoClient as PyMongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import ConnectionException, InvalidParameterException


class MongoDB:
    @classmethod
    def _get_client(cls) -> PyMongoClient:
        try:
            return PyMongoClient(
                host=settings.MONGODB_HOST,
                port=settings.MONGODB_PORT,
                username=settings.MONGODB_USERNAME,
                password=settings.MONGODB_PASSWORD,
                readPreference="primary",
                directConnection=True,
                tls=settings.MONGODB_TLS,
                connectTimeoutMS=settings.MONGODB_CONNECTION_TIMEOUT_SECONDS * 1000,
                minPoolSize=settings.MONGODB_MIN_CONNECTION_POOL_SIZE,
                maxPoolSize=settings.MONGODB_MAX_CONNECTION_POOL_SIZE,
            )
        except PyMongoError as exc:
            raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc

    @classmethod
    def _get_db(
        cls,
        db_name: str = settings.MONGODB_DB_NAME,
        client: PyMongoClient | None = None,
    ) -> Database:
        if not client:
            client = cls._get_client()

        try:
            db: Database = client[db_name]
            db.create_collection()
            return client[db_name]
        except Exception as exc:
            raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc

    @classmethod
    def get_collection(
        cls,
        collection_name: str,
        db: Database | None = None,
        db_name: str = settings.MONGODB_DB_NAME,
    ) -> Collection:

        if collection_name not in settings.MONGODB_COLLECTIONS:
            raise InvalidParameterException(ErrorCode.INVALID_COLLECTION)

        if not db:
            db = cls._get_db(db_name=db_name)

        if collection_name not in db.list_collection_names():
            try:
                db.create_collection(name=collection_name, check_exists=False)
            except PyMongoError as exc:
                raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc

        try:
            collection: Collection = db[collection_name]
        except Exception as exc:
            raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc

        try:
            collection_indexes: dict = collection.index_information()
            index_fields = [
                index_pair
                for _, index_info in collection_indexes
                for index_pair in index_info["key"]
            ]

            for collection_index_pair in settings.MONGODB_COLLECTIONS[collection_name]:
                if collection_index_pair not in index_fields:
                    collection.create_index(keys=[collection_index_pair], unique=True)

        except Exception as exc:
            raise ConnectionException(ErrorCode.DATABASE_DOWN) from exc

        return collection
