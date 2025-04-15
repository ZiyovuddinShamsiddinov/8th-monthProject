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

from rest_framework import serializers
from django.contrib.auth import authenticate

from .login_serializers import UserSerializer
from ..models.auth_user import *
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.model_student import *
from rest_framework import serializers
from configapp.models.auth_user import User
from configapp.models.model_teacher import Teacher


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'user', 'group',"descriptions"]

class StudentUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id','phone_number','password','email','is_active','is_teacher','is_staff','is_admin','is_student')


class StudentPostSerializer(serializers.Serializer):
    user=StudentUserSerializer()
    student=StudentSerializer()