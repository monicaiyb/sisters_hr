from django.shortcuts import render
from django.contrib.auth.models import Group, User
from employees.models import Employee,Attendance,LeaveManagement
from rest_framework import (
    authentication, 
    permissions, 
    parsers, 
    throttling, 
    renderers,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.serializers import EmployeeSerializer, AttendenceSerializer, LeaveManagementSerializer

class EmployeeList(APIView):
  
    def get(self, request, format=None):
        items = Employee.objects.all()
        serializer = EmployeeSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = EmployeeSerializer(item)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = EmployeeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AttendanceListCreateView(APIView):
    """This class defines the create behavior of our rest api."""

    def get(self, request, format=None):
        """Retrieves the list of attendance. """
        items = Attendance.objects.all()
        serializer = AttendenceSerializer(items, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """Save the post data when creating a new attenance."""
        serializer = AttendenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceRetrieveUpdateDestroyView(APIView):
    """This class handles the http GET, PUT and DELETE requests."""

    def get(self, request, pk, format=None):
        """Retrieves a single attendance."""
        item = self.get_object(pk)
        serializer = AttendenceSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Updates a single attendance record."""
        item = self.get_object(pk)
        serializer = AttendenceSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Deletea single attendeance record."""
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)