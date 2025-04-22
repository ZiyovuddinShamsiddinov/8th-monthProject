from msilib.schema import Registry
from django.urls import path

from .views.attendance import AttendanceApi
from .views.login import *
from .views.teacher_views import *
from .views.student_views import *
from .views.group_views import *



urlpatterns = [
    path('auth/login/', LoginApi.as_view(), name='login'),
    path('post_phone_send_otp/', PhoneSendOTP.as_view()),
    path('post_phone_v_otp/', VerifySMS.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('teacher_add/',TeacherApi.as_view()),
    path('student_add/',StudentApi.as_view()),
    path('student_update/',StudentUpdate.as_view()),
    path('group/api/',GroupApi.as_view()),
    path('teacher_update/',TeacherUpdate.as_view()),
    path('attendance/',AttendanceApi.as_view()),

]
