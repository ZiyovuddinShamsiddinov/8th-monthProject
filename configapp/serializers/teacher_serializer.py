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


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'departments',"course","descriptions"]

class TeacherUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id','phone_number','password','email','is_active','is_teacher','is_staff','is_admin','is_student')


class TeacherPostSerializer(serializers.Serializer):
    user=TeacherUserSerializer()
    teacher=TeacherSerializer()