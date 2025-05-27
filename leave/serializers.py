from .models import LeaveManagement
from rest_framework import serializers

class LeaveManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagement
        fields = '__all__'