from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('employees', views.EmployeeViewSet, basename='employees')

urlpatterns = [
    path('students/', views.StudentsView), 
    path('students/<int:pk>/', views.StudentDetailsView), 
    
    # path('employees/', views.Employees.as_view()),
    # path('employees/<int:pk>/', views.EmployeeDetails.as_view()),
    
    path('', include(router.urls)),
    
    path('blogs/', views.BlogView.as_view()),
    path('comments/', views.CommentsView.as_view()),
    # path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyView.as_view()),
]