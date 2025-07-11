from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from leave.views import EmployeeList, EmployeeDetail

urlpatterns = [
    path('leave', EmployeeList.as_view()),
    path('leave/<pk>', EmployeeDetail.as_view()),
]