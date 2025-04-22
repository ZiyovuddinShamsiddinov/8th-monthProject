from django.contrib import admin
from .models import *
from .models.model_attendance import Attendance
from .models.model_group import *
from .models.model_student import *
from .models.auth_user import *
from .models.model_teacher import *

admin.site.register([Rooms,TableType,Table,GroupStudent,Student,Parents,User,Course,Departments,Teacher,Attendance])