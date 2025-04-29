from django.db import models

from configapp.models.model_group import GroupStudent
from configapp.models.model_teacher import Teacher


class Lesson(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    group = models.ManyToManyField(GroupStudent)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

