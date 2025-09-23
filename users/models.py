from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager for custom user model that uses email as the unique identifier."""

    def create_user(self, email, name=None, password=None, **extra_fields):
        """Create and save a regular user with the given email and name.
        If no name is provided, use the first part of the email before '@'.
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        if not name:
            name = email.split("@")[0]

        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name=None, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email as the username field.

    Fields:
    - email (unique) - used for authentication
    - name - full name (defaults to first part of email if not provided)
    - image - optional ImageField storing profile pictures
    - balance, income_total, expense_total - financial tracking fields
    - date_joined - timestamp when account was created
    - is_active, is_staff - standard flags
    """

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    # New financial fields
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    income_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    expense_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split(" ")[0] if self.name else self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
