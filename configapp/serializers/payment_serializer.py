from rest_framework import serializers
from ..models.model_payments import *

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['date', 'student']  # Make student read-only

    def create(self, validated_data):
        # Automatically set student from the request user
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)