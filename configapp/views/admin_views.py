from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .add_permission import IsAdminPermission
from ..serializers.admin_serializer import AdminSerializer
from ..serializers.login_serializers import UserSerializer
from .add_pegination import *  # <-- импортируем пагинацию

User = get_user_model()

class UserManagementApi(APIView):
    permission_classes = [IsAdminPermission]

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': True, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all()
        paginator = CustomPagination()  # <-- подключаем paginator
        result_page = paginator.paginate_queryset(users, request)
        serializer = AdminSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': True, 'message': 'User updated successfully'})

    @swagger_auto_schema(request_body=UserSerializer)
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'status': True, 'message': 'User deleted successfully'})
