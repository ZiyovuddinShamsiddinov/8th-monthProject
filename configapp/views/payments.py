from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models.model_payments import *
from ..serializers.payment_serializer import PaymentSerializer
from .add_pegination import CustomPagination  # Импорт пагинации

class PaymentListCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # student id POST orqali beriladi
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        payments = Payment.objects.all()
        paginator = CustomPagination()  # Создаем объект пагинации
        result_page = paginator.paginate_queryset(payments, request)  # Применяем пагинацию
        return paginator.get_paginated_response(PaymentSerializer(result_page, many=True).data)  # Возвращаем пагинированный ответ

class MyPaymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(student=request.user)
        paginator = CustomPagination()  # Создаем объект пагинации
        result_page = paginator.paginate_queryset(payments, request)  # Применяем пагинацию
        return paginator.get_paginated_response(PaymentSerializer(result_page, many=True).data)  # Возвращаем пагинированный ответ
