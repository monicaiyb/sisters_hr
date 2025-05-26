from rest_framework import serializers
from django.contrib.auth.models import Group, User
from employees.models import Employee, Attendance, LeaveManagement

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


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceTotal
        fields = '__all__'


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignTime
        fields = '__all__'
    