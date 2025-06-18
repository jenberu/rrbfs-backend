from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class IsHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_hr() or request.user.is_admin())

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employee()

class IsOwnerOrDepartmentHR(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        if request.user.is_hr() and obj.department == request.user.department:
            return True
        return obj.uploaded_by == request.user