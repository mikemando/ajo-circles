import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal

class UserManager(BaseUserManager):
    def create_user(self, phone_number, bvn, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Enter a valid Phone number")
        
        if not bvn:
            raise ValueError("Enter a valid BVN")

        user = self.model(phone_number=phone_number, bvn=bvn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254)
    phone_number = models.CharField(unique=True, max_length=15)
    bvn = models.CharField(unique=True, max_length=11)
    credit_score = models.CharField(max_length=3)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number
    

class PhoneNumberVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    otp = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Wallet of {self.user_id.username}"


class Circle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=254)
    goal_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    current_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CircleMembership(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return f"{self.user_id} is {self.role} of {self.circle_id}"


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} of {self.amount} by {self.user}"


class CircleTransaction(models.Model):
    TYPE_CHOICES = (
        ('contribution', 'Contribution'),
        ('withdrawal', 'Withdrawal'),
    )

    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='circle_transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='circle_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} of {self.amount} in {self.circle.name} by {self.user.username}"


class CirclePermission(models.Model):
    pass