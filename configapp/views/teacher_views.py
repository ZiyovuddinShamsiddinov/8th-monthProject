from rest_framework.permissions import IsAuthenticated  # Добавляем импорт
from functools import cache
from django.shortcuts import get_object_or_404
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


from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from ..models.model_teacher import Teacher
from ..serializers.teacher_serializer import TeacherPostSerializer, TeacherSerializer
from ..serializers.login_serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..serializers.login_serializers import *
from ..serializers.teacher_serializer import *
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..serializers.login_serializers import *
from ..serializers.teacher_serializer import *
from ..models.auth_user import *
from ..models.model_teacher import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from ..serializers.teacher_serializer import TeacherPostSerializer
from ..models.model_teacher import Teacher
from .add_pegination import *

class TeacherApi(APIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        data = {"success": True}

        # Validatsiya qilish
        serializer = TeacherPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data.get('user')
        teacher_data = serializer.validated_data.get('teacher')

        # Parolni hash qilish
        user_data['password'] = make_password(user_data['password'])
        user_data['is_active'] = True
        user_data['is_teacher'] = True

        # User yaratish
        user = User.objects.create(**user_data)

        # ManyToMany fieldlarni ajratib olish
        departments = teacher_data.pop('departments', [])
        courses = teacher_data.pop('course', [])

        # Teacher yaratish
        teacher = Teacher.objects.create(user=user, **teacher_data)

        # ManyToMany fieldlarni set qilish
        teacher.departments.set(departments)
        teacher.course.set(courses)

        data["user"] = UserSerializer(user).data
        data["teacher"] = TeacherSerializer(teacher).data

        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: TeacherPostSerializer(many=True)})
    def get(self, request):
        teacher = Teacher.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(teacher, request)
        serializer = TeacherPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TeacherUpdate(APIView):

    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        teacher.delete()
        return Response({'status': True, 'message': 'Teacher deleted successfully'})
