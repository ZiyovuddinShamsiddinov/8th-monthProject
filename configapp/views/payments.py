from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models.model_payments import Payment
from ..serializers.payment_serializer import PaymentSerializer
from .add_pegination import CustomPagination

class PaymentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        payments = Payment.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(payments, request)
        return paginator.get_paginated_response(PaymentSerializer(result_page, many=True).data)

class MyPaymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
    def get(self, request):
        payments = Payment.objects.filter(student=request.user)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(payments, request)
        return paginator.get_paginated_response(PaymentSerializer(result_page, many=True).data)