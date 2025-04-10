from tkinter.constants import CASCADE
from django.db import models
from .auth_user import *

class Student(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    group=models.ManyToManyField('GroupStudent',related_name='get_group')
    is_line=models.BooleanField(default=False)
    descriptions=models.CharField(max_length=500,blank=True,null=True)

class Parents(BaseModel):
    student=models.ManyToManyField(Student,related_name='student')
    full_name=models.CharField(max_length=150, blank=True, null=True)
    phone_number=models.CharField(max_length=13, blank=True, null=True)
    addres=models.CharField(max_length=150, blank=True, null=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

