from emp.models import MyUser
from rest_framework.test import APITestCase
from emp.serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate

class UserSerializerTestCase(APITestCase):
    def test_user_creation(self):
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_missing_email(self):
        data = {
            "password": "strongpassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0], "This field is required.")

    def test_missing_password(self):
        data = {
            "email": "testuser@example.com"
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "This field is required.")

    def test_password_write_only(self):
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid()
        user_data = serializer.data

        # Verify that 'password' is not included in the serialized output
        self.assertNotIn("password", user_data)
    
class UserLoginSerializerTest(APITestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )

    def test_login_success(self):
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = authenticate(email=data['email'], password=data['password'])
        self.assertIsNotNone(user)

    def test_invalid_email(self):
        data = {
            "email": "invalidemail.com",
            "password": "strongpassword123"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0], "Enter a valid email address.")

    def test_missing_email(self):
        data = {
            "password": "strongpassword123"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0], "This field is required.")

    def test_missing_password(self):
        data = {
            "email": "testuser@example.com"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "This field is required.")

    def test_login_failure_invalid_password(self):
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            print("Authentication failed: Invalid email or password.")
        