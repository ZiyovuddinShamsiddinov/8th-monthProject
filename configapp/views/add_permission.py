from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return request.user.is_admin

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_teacher

class TeacherPatchAndGet(BasePermission):
    def has_permission(self, request, view):
        return request.method in ["PUT","DELETE"]
