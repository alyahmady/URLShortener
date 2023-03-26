from bson import ObjectId
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from URLShortener.error_codes import ErrorCode
from URLShortener.exceptions import InvalidDataException, DuplicateEntityException
from URLShortener.utils import jsonable_encoder, validate_password_string
from users_app.models import UserCollection


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, max_length=100)
    last_name = serializers.CharField(required=False, max_length=100)

    password = PasswordField(required=True, max_length=100)
    confirm_password = PasswordField(required=True, max_length=100)

    email = serializers.EmailField(max_length=320)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise InvalidDataException(ErrorCode.PASSWORD_NOT_MATCH)

        raw_password = data.pop("confirm_password")
        validate_password_string(password=raw_password, raise_exc=True)

        return super().validate(data)

    def save(self):
        # TODO change `is_active` hard-codded value after implementing ...
        #  User Email verification or for User passive deletion

        raw_password = self.validated_data.pop("password")
        user_validated_data = self.validated_data | {
            "created_at": timezone.now(),
            "is_active": True,
            "hashed_password": make_password(raw_password),
        }

        try:
            user_db_object: InsertOneResult = UserCollection.insert_one(
                user_validated_data
            )
        except DuplicateKeyError:
            raise DuplicateEntityException(ErrorCode.DUPLICATE_USER)

        user_id = user_db_object.inserted_id
        if not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)

        user: dict = UserCollection.find_one(
            filter={"_id": user_id},
            projection={
                "_id": True,
                "first_name": True,
                "last_name": True,
                "email": True,
                "created_at": True,
                "is_active": True,
            },
        )
        return jsonable_encoder(user)
