from functools import cache
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import password_changed
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .add_permission import AdminPermission
from ..models.model_student import *
from ..models.model_group import *
from ..models.auth_user import *
from ..serializers.admin_serializer import AdminSerializer
from ..serializers.login_serializers import *
from ..serializers.student_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class AdminApi(APIView):
    permission_classes = [AllowAny,AdminPermission]

    def post(self,request):
        serializer=AdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status':True,
            })