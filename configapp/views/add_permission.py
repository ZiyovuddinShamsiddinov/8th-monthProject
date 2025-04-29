from rest_framework.permissions import BasePermission

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user  and request.user.is_admin   #and request.user.is_authenticated

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_teacher

class TeacherPatchAndGet(BasePermission):
    def has_permission(self, request, view):
        return request.method in ["PUT","DELETE"]

class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
