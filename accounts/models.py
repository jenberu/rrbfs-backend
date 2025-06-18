from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
#user model
class CustomUser(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='EMPLOYEE')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_hr(self):
        return self.role == 'HR'
    
    def is_employee(self):
        return self.role == 'EMPLOYEE'