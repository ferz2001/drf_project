from rest_framework import permissions


# class IsAdmin(permissions.BasePermission):

#     def has_permission(self, request, view, obj):
#         return request.user.is_authenticated and request.user.rcdole == 'ADMIN'

#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user


class IsModerator(permissions.BasePermission):
    message = 'Не хватает прав, нужны права Модератора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(permissions.BasePermission):
    message = 'Не хватает прав, нужны права Администратора Django'

    def has_permission(self, request, view):
        print(request.user.is_superuser)
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        print(request.user.is_superuser)
        return request.user.is_authenticated and request.user.is_superuser
