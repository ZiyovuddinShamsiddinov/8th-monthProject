from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi  # drf-yasg kutubxonasidan import
from configapp.models.model_attendance import Attendance
from ..serializers.attendance_serializer import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .add_pegination import *
from .add_permission import *


class GroupStudentAttendanceApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]  # Changed from AllowAny

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="Yo'qlama sanasi (YYYY-MM-DD)",
                          type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        date = request.GET.get('date')
        if not date:
            return Response({"error": "date parametri kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        attendances = Attendance.objects.filter(date=date).select_related('student', 'group')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    @swagger_auto_schema(request_body=AttendanceSerializer)
    def put(self, request):  # Добавлен PUT метод для админа
        if not request.user.is_admin:
            return Response({"error": "Admin huquqi kerak!"}, status=403)

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Дата уже валидна и преобразована в datetime.date
        date = serializer.validated_data['date']
        group = serializer.validated_data['group']
        absent_students = serializer.validated_data.get('absent_students', [])

        # Создаем записи посещаемости
        students = group.students.all()
        attendances = [
            Attendance(
                group=group,
                date=date,  # Передаем объект date напрямую
                student=student,
                status=student.id not in absent_students
            )
            for student in students
        ]

        Attendance.objects.bulk_create(attendances)
        return Response({"success": True}, status=201)