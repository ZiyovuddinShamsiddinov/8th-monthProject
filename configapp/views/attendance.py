from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from configapp.models.model_student import Student
from configapp.models.model_group import *
from configapp.models.model_attendance import Attendance
from ..serializers.attendance_serializer import AttendanceSerializer


class GroupAttendanceApi(APIView):
    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        """
        POST so'rovi: kelmagan studentlarni ko'rsatish va kelganlarni `status=True` qilib yozish.
        """
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            group_id = serializer.validated_data['group_id']
            date = serializer.validated_data['date']
            absent_students = serializer.validated_data.get('absent_students', [])

            try:
                group = Group.objects.get(pk=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            students = Student.objects.filter(group=group)

            # Kelmaganlarni olish
            absent_students_query = students.filter(id__in=absent_students)
            absent_ids = absent_students_query.values_list('id', flat=True)

            # Kelganlarni topish
            present_students_query = students.exclude(id__in=absent_ids)

            # Attendance yaratish
            attendances = []
            for student in students:
                status_value = student.id not in absent_ids
                attendances.append(Attendance(
                    student=student,
                    date=date,
                    status=status_value
                ))

            # Bulk create attendance records
            Attendance.objects.bulk_create(attendances)

            return Response({
                "success": True,
                "message": f"{students.count()} ta student uchun yo‘qlama yozildi",
                "present_count": present_students_query.count(),
                "absent_count": absent_students_query.count()
            }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)})
    def get(self, request, group_id):
        """
        GET so'rovi: guruh va sana bo'yicha yo'qlama ro'yxatini olish.
        """
        teacher = Teacher.objects.get(user=user)
        groups = GroupStudent.objects.filter(teacher=teacher)
        date = request.GET.get('date')
        if not date:
            return Response({"error": "date parametri kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group topilmadi"}, status=status.HTTP_404_NOT_FOUND)

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
