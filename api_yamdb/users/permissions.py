from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import User


class IsAdmin(BasePermission):
    allowed_role = "admin"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == self.allowed_role:
                return True
        return False


class IsModerator(BasePermission):
    allowed_role = "moderator"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == self.allowed_role:
                return True
        return False


class IsUser(BasePermission):
    allowed_role = "user"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == self.allowed_role:
                return True
        return False
