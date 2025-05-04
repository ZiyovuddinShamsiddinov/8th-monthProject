from rest_framework.permissions import BasePermission
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from configapp.models.model_teacher import *

class MyAdminSite(AdminSite):
    site_header = _("Моя Админка")

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated and request.user.is_admin

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_admin') and request.user.is_admin

class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and hasattr(user, 'is_teacher') and user.is_teacher


class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_admin or hasattr(request.user, 'teacher')))