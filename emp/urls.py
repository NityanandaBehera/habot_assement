from django.urls import path
from emp.views import *

urlpatterns = [
    path('',UserRegistration.as_view(),name="/"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
]
