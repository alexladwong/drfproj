from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse

from employee.models import Employee
from studentsapps.models import Student
from .serializers import EmployeeSerializer, StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db import IntegrityError
from rest_framework import mixins, generics, viewsets

# Create your views here.
@api_view(['GET', 'POST'])
def StudentsView(request):
    if request.method == 'GET':
        # Get all students from the database and serialize them into JSON format
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Create a new student from the request data and serialize it into JSON format
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def StudentDetailsView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': # 
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE': # 
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            

# Employee Satandard Class View Model
# class Employees(APIView):
#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# # EmployeeDetails
# class EmployeeDetails(APIView):
#     def get(self, request, pk):
#         try:
#             employee = Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     # Put Employee Details
#     def put(self, request, pk):
#         employee = get_object_or_404(Employee, pk=pk)
        
#         # Enforce full update for PUT (require all fields)
#         serializer = EmployeeSerializer(employee, data=request.data, partial=False) 
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Employee updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

#         return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Delete Employee Details
#     def delete(self, request, pk):
#         employee = get_object_or_404(Employee, pk=pk)
#         try:
#             employee.delete()
#             return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         except IntegrityError:
#             return Response({"error": "Cannot delete employee with related records"}, status=status.HTTP_400_BAD_REQUEST)
        



""" 
# Mixins    
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # Get Employee
    def get(self, request):
        return self.list(request)
    
    # Post Employee
    def post(self, request):
        return self.create(request)
 
 
# Mixins    
# EmployeeDetails
class EmployeeDetails(mixins.RetrieveModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin, 
                      generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # get Employee Details
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    # Update Employee Details
    def put(self, request, pk):
        return self.update(request, pk)
    
    # Destroy Employee Details
    def delete(self, request, pk):
        return self.destroy(request, pk)
"""
        
"""
# Class-Based GenericViews
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    




class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' # pk is optional
"""
    
    
class EmployeeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    # Retrieve
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK) or Response(serializer.errors)
       
    
        
    




             

    
    
    
    
         