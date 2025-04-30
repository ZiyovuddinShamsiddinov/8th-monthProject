from rest_framework.pagination import PageNumberPagination
from .add_pegination import CustomPagination  # Импортируй твою пагинацию
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from ..serializers.group_serializer import *

class GroupApi(APIView):
    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status': True,
                'details': 'Group create'
            })

    @swagger_auto_schema(responses={200: GroupSerializer(many=True)})
    def get(self, request):
        data = {"success": True}

        # Применяем пагинацию
        group = GroupStudent.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(group, request)

        # Возвращаем ответ с пагинированными данными
        return paginator.get_paginated_response(GroupSerializer(result_page, many=True).data)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.model_student import Student
from ..models.model_teacher import Teacher
from ..serializers.student_serializer import StudentSerializer
from .add_pegination import CustomPagination

class MyStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"error": "siz o'qituvchi emassiz"}, status=status.HTTP_403_FORBIDDEN)

        # Получаем группы этого преподавателя
        groups = Group.objects.filter(teacher=teacher)

        if not groups.exists():
            return Response({"error": "sizda gruppa yo'q"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем всех студентов, состоящих в этих группах
        students = Student.objects.filter(group__in=groups).distinct()

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
