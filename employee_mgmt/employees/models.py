from django.db import models

# Create your models here.
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(max_length=15)
    joining_date = models.DateField()
    def __str__(self): return self.name
