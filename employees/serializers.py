from rest_framework import serializers
from django.contrib.auth.models import Group, User
from employees.models import Employee, Attendance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["first_name","last_name","Position","department"]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'employee']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagement
        fields = '__all__'



    