from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ к данным только для администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к данным на чтение для всех (и анонимов).
    Для редактирования - только для администратора.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к данным на чтение для всех (и анонимов).
    Для редактирования - только для автора или администрации.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        return request.user.is_admin or request.user.is_moderator
