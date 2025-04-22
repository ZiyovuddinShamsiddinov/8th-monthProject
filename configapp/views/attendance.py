# from rest_framework.response import Response
# from rest_framework.views import APIView
# from configapp.models.model_attendance import Attendance
# from configapp.serializers.attendance_serializer import AttendanceSerializer
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
#
#
# class AttendensApi(APIView):
#     @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)})
#     def get(self):
#         data = {"success": True}
#         attendance = Attendance.objects.all()
#         serializer = AttendanceSerializer(attendance, many=True)
#         data['attendance']=serializer.data
#         return Response(data=data)
#
#     @swagger_auto_schema(request_body=AttendanceSerializer)
#     def post(self, request):
#         serializer = AttendanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": True, "attendance": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class AttendanceListApi(APIView):
#     def get(self, request):
#         attendances = Attendance.objects.all().select_related('student')
#         serializer = AttendanceSerializer(attendances, many=True)
#         return Response({"students": serializer.data}, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from configapp.models.model_attendance import Attendance
from configapp.serializers.attendance_serializer import AttendanceSerializer


class AttendanceApi(APIView):
    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)})
    def get(self, request):
        attendances = Attendance.objects.all().select_related('student')
        serializer = AttendanceSerializer(attendances, many=True)
        return Response({"success": True, "attendance": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "attendance": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
