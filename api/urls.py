from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsView), 
    path('students/<int:pk>/', views.StudentDetailsView), 
]