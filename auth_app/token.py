from bson import ObjectId
from rest_framework_simplejwt.tokens import RefreshToken


class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user: dict):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """

        user_id = user.get("_id")
        if isinstance(user_id, ObjectId):
            user_id = str(user_id)

        token = cls()
        token["user_id"] = user_id

        return token
