from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", dict())
        return bool(
            user and user.get("is_active") is True and user.get("_id") is not None
        )
