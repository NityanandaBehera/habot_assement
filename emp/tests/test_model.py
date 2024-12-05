from django.test import TestCase
from emp.models import MyUser,Employee

class UserModelTest(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        password = "testpassword"

        user = MyUser.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))


    def test_create_superuser(self):
        """Test creating a superuser"""
        email = "admin@example.com"
        password = "adminpassword"

        superuser = MyUser.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password(password))

class EmployeeModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            role="analyst",
            department="engineering"
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.email, "johndoe@example.com")
        self.assertEqual(self.employee.role, "analyst")
        self.assertEqual(self.employee.department, "engineering")
        self.assertTrue(self.employee.is_active)
        self.assertIsNotNone(self.employee.date_joined)
        self.assertIsNotNone(self.employee.updated_at)

    def test_role_choices(self):
        self.employee.role = "manager"
        self.employee.save()
        self.assertEqual(self.employee.role, "manager")

        with self.assertRaises(ValueError):
            self.employee.role = "invalid_role"
            self.employee.full_clean() 

    def test_department_choices(self):
        self.employee.department = "sales"
        self.employee.save()
        self.assertEqual(self.employee.department, "sales")

        with self.assertRaises(ValueError):
            self.employee.department = "invalid_department"
            self.employee.full_clean()

    def test_string_representation(self):
        self.assertEqual(str(self.employee), "John Doe")
        