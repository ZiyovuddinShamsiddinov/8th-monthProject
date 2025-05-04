from tkinter.constants import CASCADE
from django.db import models
from .auth_user import *
from .model_group import *


class Student(BaseModel):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    group = models.ForeignKey('GroupStudent', related_name='group_students', on_delete=models.CASCADE)
    is_line=models.BooleanField(default=False)
    descriptions=models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.group.title}"


class Parents(BaseModel):
    student=models.ManyToManyField(Student,related_name='student')
    full_name=models.CharField(max_length=150, blank=True, null=True)
    phone_number=models.CharField(max_length=13, blank=True, null=True)
    addres=models.CharField(max_length=150, blank=True, null=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

