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

class AdminSerializer(serializers.Serializer):
    phone_number=serializers.CharField(max_length=150)
    is_admin =serializers.BooleanField(default=True)

    def update(self, instance, validated_data):
        # Здесь происходит обновление данных
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create(**validated_data)