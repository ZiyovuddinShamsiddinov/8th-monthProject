from functools import cache
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import password_changed
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models.model_student import *
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.auth_user import *
from ..serializers.login_serializers import *
from ..serializers.student_serializer import StudentSerializer
from ..serializers.teacher_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class StudentApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: StudentSerializer(many=True)})
    def get(self, request):
        data = {'success': True}
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        data["teacher"] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        data = {"success": True}
        user = request.data["user"]
        student = request.data["student"]
        phone_number = user["phone_number"]

        user_serialazer = UserSerializer(data=user)
        if user_serialazer.is_valid(raise_exception=True):
            user_serialazer.validated_data['password'] = make_password(user_serialazer.validated_data['password'])
            user_serialazer.validated_data['is_active'] = True
            user_serialazer.validated_data['is_teacher'] = True
            user = user_serialazer.save()

            student["user"] = user.id
            student_serializer = TeacherSerializer(data=student)
            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save()
                data["user"] = user_serialazer.data
                data["teacher"] = student_serializer.data
                return Response(data=data)
            return Response(data=student_serializer.errors)

        return Response(data=user_serialazer.errors)