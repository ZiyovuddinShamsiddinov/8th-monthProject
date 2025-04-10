from msilib.schema import Registry
from django.urls import path
from .views.login import *
from .views.teacher_crud import *
# from .views.


urlpatterns = [
    path('auth/login/', LoginApi.as_view(), name='login'),
    path('post_phone_send_otp/', PhoneSendOTP.as_view()),
    path('post_phone_v_otp/', PhoneSendOTP.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('teacher_add/',TeacherApi.as_view()),

]
