from rest_framework import permissions


class HasPermissionToDestroy(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.user == request.user
        return False
