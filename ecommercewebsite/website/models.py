from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.hashers import make_password


# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **other_fields):
        """
        Create and save a user with the given email and password. And any other fields, if specified.
        """
        if not email:
            raise ValueError('An Email address must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **other_fields)

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **other_fields)
    

class User(AbstractUser):
    username=models.CharField(max_length=100,null=True,blank=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.IntegerField(null=True)
    address=models.CharField(max_length=300,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects=UserManager()

    def get_username(self):
        return self.email 

# Create your models here.
class Notification(models.Model):
      users=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      message = models.CharField(max_length=255)
      is_read = models.BooleanField(default=False)
      created_at = models.DateTimeField(auto_now_add=True)
