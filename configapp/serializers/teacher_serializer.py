from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from configapp.models.auth_user import User
from configapp.models.model_teacher import Teacher
from configapp.models.model_group import Departments, Course


class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = True
        validated_data['is_teacher'] = True
        return User.objects.create(**validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    user = TeacherUserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'departments', 'course', 'descriptions']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        departments = validated_data.pop('departments')
        courses = validated_data.pop('course')

        user = TeacherUserSerializer().create(user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.departments.set(departments)
        teacher.course.set(courses)
        return teacher

class TeacherUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'email']

class TeacherFullUpdateSerializer(serializers.ModelSerializer):
    user = TeacherUserUpdateSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'departments', 'course', 'descriptions']
