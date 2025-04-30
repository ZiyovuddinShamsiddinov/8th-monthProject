from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models.auth_user import *
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.model_student import *
from rest_framework import serializers
from configapp.models.auth_user import User
from configapp.models.model_teacher import Teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone_number','password','email','is_active','is_staff','is_admin','is_teacher','is_student')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Departments
        fields=('id','title')


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(required=True, write_only=True)
#     new_password = serializers.CharField(required=True, write_only=True)
#     re_new_password = serializers.CharField(required=True, write_only=True)
#
#     def update(self, instance, validates_date):
#         instance.password = validates_date.get('password', instance.password)
#
#         if not validates_date['new_password']:
#             raise serializers.ValidationError({'new_pasword': 'not found'})
#
#         if not validates_date['old_password']:
#             raise serializers.ValidationError({'old_pasword': 'not found'})
#
#         if not instance.check_password(validates_date['old_password']):
#             raise serializers.ValidationError({'old_pasword': 'wrong password'})
#
#         if not validates_date['new_password'] != validates_date['re_new_password']:
#             raise serializers.ValidationError({'passwords': 'do not match'})
#
#         if validates_date['new_password'] == validates_date['re_new_password'] and instance.(
#                 validates_date['old_password']):
#             instance.set_password
#             raise serializers.ValidationError({'passwords': 'do not match'})
#
#         class Meta:
#             model=User
#             fields="__all__"
#
class SMSSerializer(serializers.Serializer):
    phone_number=serializers.CharField()

class VerifySMSSerializer(serializers.Serializer):
    phone_number=serializers.CharField()
    verification_code=serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"success": False, "details": "User does not exist"})

        auth_user = authenticate(phone_number=phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({"success": False, "detail": "Invalid phone or password"})

        attrs["user"] = auth_user
        return attrs
