from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
    ScopedRateThrottle,
)


class CustomAnonRateThrottle(AnonRateThrottle):
    scope = "anon"

    def get_cache_key(self, request, view):
        user = getattr(request, "user", dict())
        is_authenticated = bool(
            user and user.get("is_active") is True and user.get("_id") is not None
        )
        if is_authenticated:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }


class CustomUserRateThrottle(UserRateThrottle):
    scope = "user"

    def get_cache_key(self, request, view):
        user = getattr(request, "user", dict())
        is_authenticated = bool(
            user and user.get("is_active") is True and user.get("_id") is not None
        )
        if is_authenticated:
            ident = str(user["_id"])
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}


class CustomScopedRateThrottle(ScopedRateThrottle):
    scope_attr = "throttle_scope"

    def get_cache_key(self, request, view):
        user = getattr(request, "user", dict())
        is_authenticated = bool(
            user and user.get("is_active") is True and user.get("_id") is not None
        )
        if is_authenticated:
            ident = str(user["_id"])
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}
