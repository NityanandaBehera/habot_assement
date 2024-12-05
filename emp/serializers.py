from rest_framework import serializers
from emp.models import *
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],  # Corrected 'username' to 'email'
            password=validated_data['password'],
            # role=validated_data.get('role', 'analyst')  # Added role as an optional field with default
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'role', 'department', 'date_joined', 'is_active', 'updated_at','profile']
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name should not be empty.")
        return value

    def validate_email(self, value):
        # Get the ID of the instance if it's provided in the context (i.e., in updates)
        employee_id = self.instance.id if self.instance else None
        
        # Check if another employee with this email exists in the database
        if Employee.objects.filter(email=value).exclude(id=employee_id).exists():
            raise serializers.ValidationError("Email must be unique.")
        return value        