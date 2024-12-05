from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from emp.serializers import EmployeeSerializer
from emp.models import Employee
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('/') 
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'Test@1234'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], "Registration successfully")

    def test_user_registration_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data['email'] = ''
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('login')  
        self.email = 'testuser@example.com'
        self.password = 'Test@1234'
        
        # Create a user for login tests
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_user_login_success(self):
        # Test login with valid credentials
        response = self.client.post(self.url, {'email': self.email, 'password': self.password}, format='json')
        
        # Check for successful login response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['msg'], "User login successfully")

    def test_user_login_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post(self.url, {'email': self.email, 'password': 'WrongPassword'}, format='json')
        
        # Check for unsuccessful login response
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors']['non_field_errors'], ["Email or Password is not valid"])

    def test_user_login_missing_fields(self):
        # Test login with missing fields
        response = self.client.post(self.url, {'email': self.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmployeeListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(email='testuser@example.com', password='Test@1234')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # URL for the endpoint
        self.url = reverse('employee-list-create')  # Replace with your actual URL name
        
        # Sample data for creating employees
        self.valid_employee_data = {
            'name': 'John Doe',
            'email': 'test@gmail.com',
            
        }
        self.invalid_employee_data = {
            'name': '',
            'email': 'te@gmail.com'
        }

        # Create multiple employees for pagination testing
        Employee.objects.bulk_create([
            Employee(name='Employee 1', email='test1@gmail.com'),
            Employee(name='Employee 2', email='test2@gmail.com'),
            # Add more employees if needed for pagination
        ])

    def test_get_employee_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), min(10, Employee.objects.count()))

    def test_get_employee_list_with_department_filter(self):
        response = self.client.get(self.url, {'department': 'HR'}, format='json')
        
        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that all returned employees are in the specified department
        for employee in response.data['results']:
            self.assertEqual(employee['department'], 'HR')

    def test_create_employee_success(self):
        response = self.client.post(self.url, self.valid_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.valid_employee_data['name'])

    def test_create_employee_invalid_data(self):
        response = self.client.post(self.url, self.invalid_employee_data, format='json')
        
        # Check the response status for error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_get_employee_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class EmployeeDetailViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='Test@1234')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Create a test employee
        self.employee = Employee.objects.create(
            name="John Doe",
            email="testuser3@gmail.com"
        )

        # URL for the employee detail endpoint with the employee ID
        self.url = reverse('employee-detail', args=[self.employee.id])

    def test_get_employee_success(self):
        # Test retrieving the employee's details
        response = self.client.get(self.url, format='json')
        
        # Check the response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)
        self.assertEqual(response.data['department'], self.employee.department)

    def test_update_employee_success(self):
        # Test updating the employee's details
        updated_data = {
            'name': 'John Updated',
            'department': 'hr'
        }
        response = self.client.put(self.url, updated_data, format='json')
        
        # Check the response status and updated data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['department'], updated_data['department'])

    def test_delete_employee_success(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=self.employee.id)        