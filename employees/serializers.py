from rest_framework import serializers
from django.contrib.auth.models import Group, User
from employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id","first_name","last_name","Position","department"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'employee']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
    