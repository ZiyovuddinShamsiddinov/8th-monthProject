from rest_framework import serializers
from django.contrib.auth import authenticate

from .login_serializers import UserSerializer
from ..models.auth_user import *
from ..models.model_attendance import Attendance
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.model_student import *
from rest_framework import serializers
from configapp.models.auth_user import User
from configapp.models.model_teacher import Teacher

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'group', 'teacher', 'student_name', 'attended']

