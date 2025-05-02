from rest_framework.permissions import BasePermission
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class MyAdminSite(AdminSite):
    site_header = _("Моя Админка")

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated and request.user.is_admin


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

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
