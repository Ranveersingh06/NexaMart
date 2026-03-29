from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ============================================================
# CUSTOM USER MANAGER
# ============================================================
# Why: We need a custom manager because we use email
# as the login field instead of username
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


# ============================================================
# CUSTOM USER MODEL
# ============================================================
# Why: We extend Django's default user to add:
# - Email as login field (instead of username)
# - Role field (admin, seller, customer)
# - Phone number and address
class CustomUser(AbstractBaseUser, PermissionsMixin):

    # Role choices for the user
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )

    # Basic fields
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Role field
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    # Status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email} ({self.role})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'