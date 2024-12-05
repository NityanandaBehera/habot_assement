from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        blank=False
    )
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Employee(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('analyst', 'Analyst'),
    )
    DEPARTMENT_CHOICES = (
        ('engineering', 'Engineering'),
        ('hr', 'HR'),
        ('sales', 'Sales'),
    )
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        blank=False
    )
    profile=models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='analyst')
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='sales')
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at=models.DateTimeField(auto_now_add=True)    
    
    
    def __str__(self):
        return self.name