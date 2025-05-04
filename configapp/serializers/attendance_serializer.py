# serializers/attendance_serializer.py
from rest_framework import serializers
from configapp.models.model_attendance import *
from configapp.models.model_group import *
from configapp.models.model_student import *

class AttendanceSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=GroupStudent.objects.all())
    date = serializers.DateField(format='%Y-%m-%d')
    absent_students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False,
        source='absent_students.all'  # Добавлено для корректной связи
    )

    class Meta:
        model = Attendance
        fields = ['id', 'group', 'date', 'absent_students']
        extra_kwargs = {
            'absent_students': {'required': False}
        }
