from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserOrReadOnly(BasePermission):
    """Редактирование для авторов или только чтение"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
