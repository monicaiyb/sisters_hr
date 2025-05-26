from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee

class EmployeeTests(APITestCase):
	def test_create_employee(self):
		url = reverse('employee-list')
		data = {'title': 'Test employee', 'content': 'Test content'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Employee.objects.count(), 1)
		self.assertEqual(Employee.objects.get().title, 'Test Employee')

