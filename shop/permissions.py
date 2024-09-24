from rest_framework.permissions import BasePermission

# cette classe est notre permission personalisee

class IsAdminAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser )