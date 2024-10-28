from rest_framework.response import Response
from rest_framework.views import APIView
from emp.serializers import *
from django.contrib.auth import authenticate
from emp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistration(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':"Registration successfully"})    
        return Response(serializer.errors)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':"User login successfully"})
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}})
        return Response(serializer.errors)   
    
class EmployeeListCreateView(APIView):
    renderer_classes=[UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        department_filter = request.GET.get('department', None)
        employees = Employee.objects.all()
        if department_filter:
            employees = employees.filter(department__iexact=department_filter)
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    renderer_classes=[UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, id):
        return get_object_or_404(Employee, id=id)

    def get(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        employee = self.get_object(id)
        employee.delete()
        return Response({'msg':"Employee removed from this db sucessfully"},status=status.HTTP_204_NO_CONTENT)     
