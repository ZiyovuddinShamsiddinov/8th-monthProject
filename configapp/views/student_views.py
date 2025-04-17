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
from ..models.auth_user import *
from ..serializers.login_serializers import *
from ..serializers.student_serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class StudentApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: StudentSerializer(many=True)})
    def get(self, request):
        student = Student.objects.all()
        paginator = CustomPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(student, request)
        serializer = StudentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def post(self, request):
        data = {"success": True}
        user = request.data.get("user")
        student = request.data.get("student")
        user_serializer = UserSerializer(data=user)

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user_serializer.validated_data['is_active'] = True  #
            user_serializer.validated_data['is_student'] = True
            user = user_serializer.save()

            student["user"] = user.id
            student_serializer = StudentSerializer(data=student)
            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save()
                data["user"] = user_serializer.data
                data["student"] = student_serializer.data
                return Response(data=data, status=status.HTTP_201_CREATED)

            return Response(data=student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
