from tkinter.constants import CASCADE
from django.db import models
from .model_teacher import *
from .auth_user import *

class Day(BaseModel):
    title=models.CharField(max_length=150)
    descriptions=models.CharField(max_length=100 , blank=True , null=True)

class Rooms(BaseModel):
    title = models.CharField(max_length=150)
    descriptions = models.CharField(max_length=100, blank=True, null=True)

class TableType(BaseModel):
    title = models.CharField(max_length=150)
    descriptions = models.CharField(max_length=100, blank=True, null=True)

class Table(BaseModel):
    pass

class GroupStudent(BaseModel):
    title=models.CharField(max_length=150)
    course=models.ForeignKey(Course,on_delete=models.RESTRICT)
    teacher=models.ManyToManyField(Teacher)
    table=models.ManyToManyField(Table)
    start_date=models.DateField()
    end_date=models.DateField()
    descriptions=models.CharField(max_length=500,blank=True,null=True)