from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from configapp.models.model_teacher import Teacher
from configapp.views.add_permission import *
from configapp.serializers.teacher_serializer import *
from configapp.views.add_pegination import *


class TeacherApi(APIView):
    permission_classes = [IsAdminPermission, IsStaffPermission]

    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: TeacherSerializer(many=True)})
    def get(self, request):
        teachers = Teacher.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(teachers, request)
        serializer = TeacherSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TeacherUpdateApi(APIView):
    permission_classes = [IsAdminPermission, IsStaffPermission]

    def get_object(self, phone_number):
        return get_object_or_404(Teacher, user__phone_number=phone_number)

    @swagger_auto_schema(request_body=TeacherFullUpdateSerializer)
    def put(self, request, phone_number):
        teacher = self.get_object(phone_number)
        serializer = TeacherFullUpdateSerializer(teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        teacher_data = serializer.validated_data

        # Обновляем user'а
        user_data = teacher_data.pop('user', None)
        if user_data:
            user = teacher.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Обновляем ManyToMany поля
        if 'departments' in teacher_data:
            teacher.departments.set(teacher_data.pop('departments'))
        if 'course' in teacher_data:
            teacher.course.set(teacher_data.pop('course'))

        # Остальные поля
        for attr, value in teacher_data.items():
            setattr(teacher, attr, value)

        teacher.save()

        return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TeacherUserUpdateSerializer)
    def delete(self, request, phone_number):
        teacher = self.get_object(phone_number)
        teacher.delete()
        return Response({'status': True, 'message': 'Teacher deleted successfully'})
