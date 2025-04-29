from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from configapp.models.model_student import Student
from configapp.models.model_group import *
from configapp.models.model_attendance import Attendance
from ..serializers.attendance_serializer import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class GroupStudentAttendanceApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data['group']  # <- bu obyekt!
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
        GET so'rovi: guruh va sana bo'yicha yo'qlama ro'yxatini olish.
        """
        teacher = Teacher.objects.get(user=request.user)
        group = GroupStudent.objects.filter(teacher=teacher)
        date = request.GET.get('date')
        if not date:
            return Response({"error": "date parametri kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = GroupStudent.objects.get(pk=group)
        except GroupStudent.DoesNotExist:
            return Response({"error": "GroupStudent topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        students = Student.objects.filter(group__in=groups).distinct()

        # Kelmaganlarni olish
        absent_students = request.GET.getlist('absent_students[]', [])
        absent_students = list(map(int, absent_students))  # JSON'dan kelgan ro'yxatni integer ga aylantirish

        absent_students_query = students.filter(id__in=absent_students)
        absent_data = [{"id": s.id, "full_name": s.full_name} for s in absent_students_query]

        # Kelganlarni topish
        present_students_query = students.exclude(id__in=absent_students)
        present_data = [{"id": s.id, "full_name": s.full_name} for s in present_students_query]

        return Response({
            "date": date,
            "group": group.name,
            "present_count": len(present_students_query),
            "absent_count": len(absent_students_query),
            "present_students": present_data,
            "absent_students": absent_data
        }, status=status.HTTP_200_OK)
