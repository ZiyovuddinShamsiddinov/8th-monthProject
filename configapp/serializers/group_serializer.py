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

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields=["title","course","teacher","table"]