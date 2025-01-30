from django.db import models

# Create your models here.



class Employee(models.Model):
    emp_id = models.CharField(max_length=25)
    emp_name = models.CharField(max_length=55)
    designation = models.CharField(max_length=55, null=True)
    email = models.EmailField(unique=True)
    emp_phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.emp_name
