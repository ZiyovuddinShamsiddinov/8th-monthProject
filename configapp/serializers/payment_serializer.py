from rest_framework import serializers
from ..models.model_payments import *

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = 'all'
        read_only_fields = ['date']