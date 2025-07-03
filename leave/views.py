from django.shortcuts import render
from django.contrib.auth.models import Group, User
from leave.models import LeaveManagement
from rest_framework import (
    authentication, 
    permissions, 
    parsers, 
    throttling, 
    renderers,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from leave.serializers import  LeaveManagementSerializer

# Create your views here.
class EmployeeList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        items = LeaveManagement.objects.all()
        serializer = LeaveManagementSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeaveManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = LeaveManagementSerializer(item)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = LeaveManagementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


