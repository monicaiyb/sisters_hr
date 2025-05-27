import uuid
from django.db import models

# Create your models here.

sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Employee(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    Position=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    sex = models.CharField(max_length=50, choices=sex_choice, default='Male')
    DOB = models.DateField(default='1980-01-01')
    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hire_date = models.DateField(default='1980-01-01')
    owner = models.ForeignKey('auth.User', related_name='employee', on_delete=models.CASCADE)
    


    
class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default='False')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task=models.TextField()

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


