from rest_framework.permissions import SAFE_METHODS, BasePermission


def check_role(request, *args):
    if request.user.is_authenticated:
        if request.user.role in args:
            return True
        elif request.user.is_superuser:
            return True
    return False


class ReadOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or check_role(request, 'admin'))


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return check_role(request, 'admin')


class AuthorOrAdminOrModeratorOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user))
