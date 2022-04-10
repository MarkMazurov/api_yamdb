from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserOnly(BasePermission):
    """Доступ только для пользователя."""
    def has_permission(self, request, view):
        return request.user.is_user


class ModeratorOnly(BasePermission):
    """Доступ только для модератора."""
    def has_permission(self, request, view):
        return request.user.is_moderator


class AdminOnly(BasePermission):
    """Доступ только для Админа."""
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class ReadOrAdminOnly(BasePermission):
    """Доступ только для Админа или только чтение."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class AuthorOrAdminOrModeratorOnly(BasePermission):
    """Доступ только для автора, админа или модератора"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user))
