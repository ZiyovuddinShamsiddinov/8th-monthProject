from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from configapp.models.model_student import Student
from configapp.models.model_group import GroupStudent
from configapp.models.model_attendance import Attendance, Teacher
from ..serializers.attendance_serializer import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .add_pegination import CustomPagination  # <-- Пагинатор импорт

class GroupStudentAttendanceApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data['group']
        date = serializer.validated_data['date']
        absent_students = serializer.validated_data.get('absent_students', [])

        teacher = group.teacher
        students = Student.objects.filter(group=group)
        absent_ids = set(absent_students)

        attendances = [
            Attendance(
                student=student,
                group=group,
                teacher=teacher,
                date=date,
                status=(student.id not in absent_ids)
            )
            for student in students
        ]
        Attendance.objects.bulk_create(attendances)

        return Response({
            "success": True,
            "message": f"{students.count()} ta student uchun yo‘qlama yozildi",
            "present_count": students.count() - len(absent_ids),
            "absent_count": len(absent_ids)
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)})
    def get(self, request):
        """
        GET: Guruh va sana bo'yicha yo'qlama ro'yxatini olish (paginatsiya bilan)
        """
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"error": "Siz teacher emassiz!"}, status=status.HTTP_400_BAD_REQUEST)

        date = request.GET.get('date')
        if not date:
            return Response({"error": "date parametri kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        attendances = Attendance.objects.filter(group__teacher=teacher, date=date).select_related('student', 'group')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
