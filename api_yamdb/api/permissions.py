from rest_framework import permissions
from reviews.models import Comment, Review
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """
    Предоставляет права суперпользователю,
    администратору и
    аутентифицированному пользователю с ролью admin.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_admin)
        )


class AnonimReadOnly(permissions.BasePermission):
    """Предоставляет права анонимному пользователю
       только на безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ReviewCommentPermissions(permissions.BasePermission):
    """Предоставляет права на написание комментариев и отзывов.
       Разрешает анонимному пользователю только безопасные запросы.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        if ((isinstance(obj, Comment) or isinstance(obj, Review))
            and request.user.is_authenticated
                and request.user.is_moderator):
            return True
        return (obj.author == request.user
                or request.method in SAFE_METHODS)
