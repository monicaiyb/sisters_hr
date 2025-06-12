from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count  #for dashboard
from django.contrib.auth.models import Group, User
from employees.models import Employee,Attendance
from rest_framework import (
    authentication, 
    permissions, 
    parsers, 
    throttling, 
    renderers,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apiauth.permissions import IsHR
from employees.serializers import EmployeeSerializer, AttendenceSerializer

class EmployeeList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Retrieves the list of attendance. """

        date_str = request.get('date')
        status = request.get('status')

        # Convert the date string to a Python date object
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

        # Check if an attendance record already exists for the given date and employee
        existing_attendance = Attendance.objects.filter(employee=Employee, date=date)
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
    permission_classes = [IsAuthenticated]

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
    

class Dashboard(APIView):
    permission_classes = [IsAuthenticated, IsHR]

    def get(self, request):
        employee_count = Employee.objects.all().count()
        department_stats = Employee.objects.values('department').annotate(count=Count('department'))
        # Attendence Stats
        attendance_count = Attendance.objects.all().count()
        attendance_present = Attendance.objects.filter(status='Present').count()
        attendance_absent = Attendance.objects.filter(status='Absent').count()
        attendance_leave = Attendance.objects.filter(status='Leave').count()

        return Response({
                    'employee_count': employee_count,
                    'attendance_count': attendance_count,
                    'attendance_present':attendance_present,
                    'attendance_absent':attendance_absent,
                    'attendance_leave':attendance_leave
                }, status=status.HTTP_201_CREATED)