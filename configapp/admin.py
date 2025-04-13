from django.contrib import admin
from .models import *
from .models.model_group import GroupStudent
from .models.model_teacher import Teacher, Course, Departments

admin.site.register([User,Teacher,Course,Departments,GroupStudent])