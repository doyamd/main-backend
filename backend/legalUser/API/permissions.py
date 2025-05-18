from rest_framework import permissions

class IsOwnerorReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
        
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == 'admin'
        except:
            return False
        
class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admin users to access any object
        if request.user.role == 'admin':
            return True
        # Allow users to access their own data
        return obj.id == request.user.id

# is client or admin
class IsClientOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client' or request.user.role == 'admin'
    
# is attorney or admin
class IsAttorneyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'attorney' or request.user.role == 'admin'