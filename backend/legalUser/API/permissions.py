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