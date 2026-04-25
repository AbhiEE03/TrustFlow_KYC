from rest_framework import permissions

class IsReviewer(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'reviewer' role to access.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'reviewer')
