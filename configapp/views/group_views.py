from turtledemo.clock import datum
from django.contrib.admin.templatetags.admin_list import paginator_number, result_list
from django.contrib.staticfiles.views import serve
from django.core.cache import cache
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
from ..models.model_group import *
from ..models.model_student import *
from ..models.model_teacher import *
from ..models.auth_user import *
from ..serializers.group_serializer import GroupSerializer
from ..serializers.login_serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import random
from ..tokens.get_token import *
from .add_pegination import *

class GroupApi(APIView):
    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self,request):
        serializer=GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status': True,
                'details': 'Group create'
            })

    @swagger_auto_schema(responses={200: GroupSerializer(many=True)})
    def get(self, request):
        data = {"success": True}
        group = GroupStudent.objects.all()
        serializer = GroupSerializer(group, many=True)
        data["group"] = serializer.data
        return Response(data=data)