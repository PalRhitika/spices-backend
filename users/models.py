from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.core.validators import RegexValidator
# Create your models here.

class CustomUserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError("Username is required.")
    user=self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self.__db)
    return user

  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff',True)
    extra_fields.setdefault('is_superuser',True)
    return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
  user_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  full_name=models.CharField(max_length=60,null=False, blank=False)
  email=models.EmailField(null=False, blank=False, unique=True)
  phone_validator=RegexValidator(regex=r'^(\+977)?9[6-9]\d{8}$',message='Enter the valid phone number. Format: +9779847338278')
  contact_number=models.CharField(max_length=15, validators=[phone_validator])
  company_name=models.CharField(max_length=100, blank=False, null=False)
  address=models.CharField(max_length=200, null=False, blank=False)
  industry=models.CharField(max_length=100, null=False, blank=False)
  username = models.CharField(max_length=150, unique=True, null=False, blank=False)
  is_active=models.BooleanField(default=True)
  is_staff=models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)

  objects=CustomUserManager()

  USERNAME_FIELD='username'

  def __str__(self):
    return self.full_name


