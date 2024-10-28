from django.contrib import admin
from emp.models import *

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

# Register the model with the custom admin configuration
admin.site.register(MyUser, MyUserAdmin)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'department', 'date_joined', 'is_active')
    search_fields = ('name', 'email', 'role', 'department')
    list_filter = ('role', 'department', 'is_active')

# Register the model with the custom admin configuration
admin.site.register(Employee, EmployeeAdmin)