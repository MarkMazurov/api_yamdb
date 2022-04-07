from rest_framework.permissions import SAFE_METHODS, BasePermission


def check_role(request, *args):
    """Проверка роли пользователя."""
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
                or check_role(request, 'admin'))


class AdminOnly(BasePermission):
    """Доступ только для Админа."""
    def has_permission(self, request, view):
        return check_role(request, 'admin')


class UserOnly(BasePermission):
    """Доступ только для пользователя."""
    def has_permission(self, request, view):
        return check_role(request, 'user')


class ModeratorOnly(BasePermission):
    """Доступ только для модератора."""
    def has_permission(self, request, view):
        return check_role(request, 'moderator')


class AuthorOrAdminOrModeratorOnly(BasePermission):
    """Доступ для автора, админа или модератора."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user))
