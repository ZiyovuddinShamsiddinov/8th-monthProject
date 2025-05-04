from email.headerregistry import Group
from django.db import models
from configapp.models.auth_user import BaseModel
from .model_group import GroupStudent
from .model_lesson import Lesson
from .model_student import *
from .model_teacher import Teacher

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student} - {'Kelgan' if self.attended else 'Kelmagan'}"