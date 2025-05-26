# APIView

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from employees.views import EmployeeList, EmployeeDetail

urlpatterns = [
    path('employee', EmployeeList.as_view()),
    path('employee/<pk>', EmployeeDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)