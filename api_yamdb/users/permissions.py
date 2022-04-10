from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOrAdminOnly(BasePermission):
    """Доступ только для Админа или только чтение."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_admin)


class AdminOnly(BasePermission):
    """Доступ только для Админа."""
    def has_permission(self, request, view):
        return request.user.is_admin


class UserOnly(BasePermission):
    """Доступ только для пользователя."""
    def has_permission(self, request, view):
        return request.user.is_user


class ModeratorOnly(BasePermission):
    """Доступ только для модератора."""
    def has_permission(self, request, view):
        return request.user.is_moderator
