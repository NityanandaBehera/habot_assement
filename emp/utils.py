from faker import Faker
from .models import Employee

fake = Faker()

def generate_employee(num):
    for _ in range(num):
        name = fake.name()[:100] 
        email = fake.unique.email()[:255]
        
        employee = Employee.objects.create(
            name=name,
            email=email
        )
        employee.save()
