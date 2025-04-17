from functools import cache

from django.conf.global_settings import TEST_NON_SERIALIZED_APPS
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import password_changed
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .add_permission import *
from ..models.model_student import *
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.auth_user import *
from ..serializers.login_serializers import *
from ..serializers.teacher_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class TeacherApi(APIView):
    permission_classes = [AllowAny,TeacherPermission,TeacherPatchAndGet]

    @swagger_auto_schema(responses={200: TeacherSerializer(many=True)})
    def get(self, request):
        teacher = Teacher.objects.all()
        paginator = CustomPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(teacher, request)
        serializer = TeacherSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        data = {"success": True}
        user = request.data.get("user")
        teacher = request.data.get("teacher")
        #phone_number=user["phone_number]
        user_serializer = UserSerializer(data=user)

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user_serializer.validated_data['is_active'] = True #
            user_serializer.validated_data['is_teacher'] = True
            user = user_serializer.save()

            teacher["user"] = user.id
            teacher_serializer = TeacherSerializer(data=teacher)
            if teacher_serializer.is_valid(raise_exception=True):
                teacher_serializer.save()
                data["user"] = user_serializer.data
                data["teacher"] = teacher_serializer.data
                return Response(data=data, status=status.HTTP_201_CREATED)

            return Response(data=teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)