from functools import cache
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import password_changed
from django.db.models.fields import return_None
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
# from tutorial.quickstart.serializers import UserSerializer
from ..models.model_student import *
from ..models.model_group import *
from ..models.model_teacher import *
from ..models.auth_user import *
from ..serializers.login_serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class TeacherApi(APIView):
    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self,request):
        serializer=TeacherSerializer
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Teacher added soccessfully'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)