from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import random
import datetime


class CustomerUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Username kiritilishi shart!")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)  # <-- bu ham shart
        extra_fields.setdefault('is_active', True)     # <-- bu

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser is_admin=True bo'lishi kerak!")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo'lishi kerak!")
        print("User yaratildi")
        return self.create_user(phone_number,  password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


    objects = CustomerUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
    

class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        code = str(random.randint(100000, 999999))  # 6 xonali kod
        self.otp = code
        self.created_at = timezone.now()
        self.save()
        return code

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"
    
class Movie(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    photo = models.ImageField(upload_to='photos/%Y/%m%d/', null=True, blank=True)
    genre = models.CharField(max_length=50)
    actor = models.ManyToManyField('Actor')

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=150)
    birthdate = models.DateField()

    def __str__(self):
        return self.name

class CommitMovie(models.Model):
    title = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_ed = models.DateTimeField(auto_now_add=True)
    updated_ed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
