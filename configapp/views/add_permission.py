from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin == True

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher == True

class TeacherPatchAndGet(BasePermission):
    def has_permission(self, request, view):
        return request.method in ["PUT","DELETE"]

