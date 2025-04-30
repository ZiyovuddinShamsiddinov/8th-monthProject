from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100