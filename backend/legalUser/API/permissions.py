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
        try:
            return request.user.role == 'admin' or obj.id == request.user.id
        except:
            return False

# is client or admin
class IsClientOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == 'client' or request.user.role == 'admin'
        except:
            return False
    
# is client or admin or owner
class IsClientOrAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return request.user.role == 'client' or request.user.role == 'admin' or obj.id == request.user.id
        except:
            return False
    
# is attorney or admin
class IsAttorneyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == 'attorney' or request.user.role == 'admin'
        except:
            return False
        
# is client or admin or attorney
class IsClientOrAdminOrAttorney(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == 'client' or request.user.role == 'admin' or request.user.role == 'attorney'
        except:
            return False