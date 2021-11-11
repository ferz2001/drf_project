from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
from rest_framework import permissions


class AuthADMMODOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user,
            request.user in ['ADMIN', 'MODERATOR']
        )
