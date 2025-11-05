from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CanLikeContent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.user == request.user
        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff