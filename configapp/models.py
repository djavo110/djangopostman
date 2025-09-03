from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser


class CustomerUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username kiritilishi shart!")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser is_admin=True bo'lishi kerak!")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo'lishi kerak!")
        
        return self.create_user(username,  password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


    objects = CustomerUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    @property
    def is_superuser(self):
        return self.is_admin

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
