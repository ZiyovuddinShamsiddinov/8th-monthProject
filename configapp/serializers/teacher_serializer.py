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
        fields = ['id', 'departments',"course","descriptions"]

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
    user = TeacherUserSerializer()
    teacher = TeacherSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        teacher_data = validated_data.pop('teacher')

        # User yaratish
        user = User.objects.create(
            phone_number=user_data['phone_number'],
            email=user_data.get('email', ''),
            password=make_password(user_data['password']),
            is_active=True,
            is_teacher=True
        )

        # Teacher yaratish, user ni biriktirib
        teacher = Teacher.objects.create(
            user=user,
            descriptions=teacher_data.get('descriptions', '')
        )

        # ManyToMany uchun: departments va course
        teacher.departments.set(teacher_data.get('departments', []))
        teacher.course.set(teacher_data.get('course', []))
        teacher.save()

        return teacher


class TeacherPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['departments', "course", "descriptions"]
