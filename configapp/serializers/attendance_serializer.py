# serializers/attendance_serializer.py
from rest_framework import serializers
from configapp.models.model_attendance import *
from configapp.models.model_group import *

class AttendanceSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=GroupStudent.objects.all()
    )
    date = serializers.DateField()
    absent_students = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
