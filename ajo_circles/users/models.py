import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone_number, bvn, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Enter a valid Phone number")
        
        if not bvn:
            raise ValueError("Enter a valid BVN")

        user = self.model(phone_number=phone_number, bvn=bvn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, phone_number, bvn, password=None, **extra_fields):
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, bvn, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254)
    phone_number = models.CharField(unique=True, max_length=15)
    bvn = models.CharField(unique=True, max_length=11)
    credit_score = models.CharField(max_length=3)

    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = ["phone_number"]
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number
    

class Circle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

