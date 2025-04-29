from msilib.schema import Registry
from django.urls import path
from .views.attendance import *
from .views.login import *
from .views.teacher_views import *
from .views.student_views import *
from .views.group_views import *
from .views.admin_views import *
from .views.payments import *

urlpatterns = [
    path('auth/login/', LoginApi.as_view(), name='login'),
    path('post_phone_send_otp/', PhoneSendOTP.as_view()),
    path('post_phone_v_otp/', VerifySMS.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('teacher_api/', TeacherApi.as_view()),
    path('teacher_update/', TeacherUpdate.as_view()),
    path('student_api/', StudentApi.as_view()),
    path('student_update/', StudentUpdate.as_view()),
    path('group/api/', GroupApi.as_view()),
    path('attendance/', GroupStudentAttendanceApi.as_view()),
    path('attendance/<int:group_id>/', GroupStudentAttendanceApi.as_view()),
    path('admin/crud/', UserManagementApi.as_view()),
    path('admin/crud/<int:pk>/', UserManagementApi.as_view()),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/mine/', MyPaymentsView.as_view(), name='my-payments'),
]
