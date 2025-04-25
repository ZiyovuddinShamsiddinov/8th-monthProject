from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny, ]),
)

urlpatterns = [
    path('api/', include("configapp.urls")),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('authentication /', include("authentication.urls")),
    # path('users/', include("users.urls")),
    # path('attendance/', include("attendance.urls")),
    # path('attendance_status/', include("attendance_status.urls")),
    # path('courses/', include("courses.urls")),
    # path('groups/', include("groups.urls")),
    # path('homework_reviews/', include("homework_reviews.urls")),
    # path('homework_submissions /', include("homework_submissions.urls")),
    # path('homeworks/', include("homeworks.urls")),
    # path('subjects/', include("subjects.urls")),
    # path('tables/', include("tables.urls")),
    # path('table_types/', include("table_types.urls")),
    # path('payment_types/', include("payment_types.urls")),
    # path('payments/', include("payments.urls")),
    # path('statistic/', include("statistic.urls")),
]
