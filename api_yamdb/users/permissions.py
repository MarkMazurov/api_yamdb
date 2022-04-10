from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import ADMIN, USER, MODERATOR


def check_role(request, *args):
    if request.user.is_authenticated:
        if request.user.role in args:
            return True
        elif request.user.is_superuser:
            return True
    return False


class ReadOrAdminOnly(BasePermission):
    """Доступ только для Админа или только чтение."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or check_role(request, ADMIN))


class AdminOnly(BasePermission):
    """Доступ только для Админа."""
    def has_permission(self, request, view):
        return check_role(request, ADMIN)


class UserOnly(BasePermission):
    """Доступ только для пользователя."""
    def has_permission(self, request, view):
        return check_role(request, USER)


class ModeratorOnly(BasePermission):
    """Доступ только для модератора."""
    def has_permission(self, request, view):
        return check_role(request, MODERATOR)


class AuthorOrAdminOrModeratorOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user))
