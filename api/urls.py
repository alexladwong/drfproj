from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsView), 
    path('students/<int:pk>/', views.StudentDetailsView), 
    
    path('employees/', views.Employees.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetails.as_view()),
]