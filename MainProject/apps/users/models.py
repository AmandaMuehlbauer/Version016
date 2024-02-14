# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from timezone_field.fields import TimeZoneField



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)  # The line manages the payment id
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email


#class User(AbstractUser):
 #   email = models.EmailField('email address', unique=True)
  #  username = models.CharField(max_length=30, unique=True)
   # USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ["username"]




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    about_me = models.TextField(blank=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    timezone = TimeZoneField(default='UTC')  # Set the default timezone


    def __str__(self):
        return self.user.username