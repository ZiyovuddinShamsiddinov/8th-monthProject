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
from ..serializers.teacher_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class TeacherApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: TeacherSerializer(many=True)})
    def get(self, request):
        data = {'success': True}
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        data["teacher"] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        data = {"success": True}
        user = request.data["user"]
        teacher = request.data["teacher"]
        phone_number = user["phone_number"]

        user_serialazer = UserSerializer(data=user)
        if user_serialazer.is_valid(raise_exception=True):
            user_serialazer.validated_data['password'] = make_password(user_serialazer.validated_data['password'])
            user_serialazer.validated_data['is_active'] = True
            user_serialazer.validated_data['is_teacher'] = True
            user = user_serialazer.save()

            teacher["user"] = user.id
            teacher_serializer = TeacherSerializer(data=teacher)
            if teacher_serializer.is_valid(raise_exception=True):
                teacher_serializer.save()
                data["user"] = user_serialazer.data
                data["teacher"] = teacher_serializer.data
                return Response(data=data)
            return Response(data=teacher_serializer.errors)

        return Response(data=user_serialazer.errors)


        # serializer = TeacherSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     data["data"] = serializer.data
        #     return Response(data=data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
