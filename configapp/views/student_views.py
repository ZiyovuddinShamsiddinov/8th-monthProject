from functools import cache
from django.shortcuts import get_object_or_404
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
from ..models.auth_user import *
from ..serializers.login_serializers import *
from ..serializers.student_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .add_pegination import CustomPagination  # Импорт пагинации


class StudentApi(APIView):
    permission_classes = [IsStaffPermission,IsAdminPermission]

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def post(self, request):
        data = {"success": True}
        user_data = request.data.get("user")
        student_data = request.data.get("student")

        # Проверка на существование пользователя
        if User.objects.filter(phone_number=user_data['phone_number']).exists():
            return Response({'error': 'User with this phone number already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем пользователя
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user_serializer.validated_data['is_active'] = True
            user_serializer.validated_data['is_student'] = True
            user = user_serializer.save()

            # Проверяем группу
            group = student_data.get('group')
            if not GroupStudent.objects.filter(id=group).exists():
                return Response({'error': 'Group not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Создаем студента
            student_serializer = StudentSerializer(data=student_data)
            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save(user=user)  # Вот здесь привязываем пользователя
                data["user"] = user_serializer.data
                data["student"] = student_serializer.data
                return Response(data=data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: StudentSerializer(many=True)})
    def get(self, request):
        students = Student.objects.all()
        paginator = CustomPagination()  # Создаем объект пагинации
        paginator.page_size = 2  # Задаем количество элементов на странице
        result_page = paginator.paginate_queryset(students, request)  # Применяем пагинацию
        serializer = StudentSerializer(result_page, many=True)  # Сериализуем пагинированные данные
        return paginator.get_paginated_response(serializer.data)  # Возвращаем пагинированный ответ


class StudentUpdate(APIView):
    permission_classes = [IsStaffPermission, IsAdminPermission]

    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentSerializer)
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({'status': True, 'message': 'Student deleted successfully'})
