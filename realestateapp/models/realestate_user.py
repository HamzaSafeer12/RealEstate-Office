from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('investor', 'Investor'),
        ('developer', 'Developer'),
        ('realtor', 'Realtor'),
    ]

    # Removing uniqueness constraint from username
    username = models.CharField(max_length=100, blank=True, null=True)  # Optional and non-unique username
    email = models.EmailField(unique=True)  # Email as unique login field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    company_name = models.CharField(max_length=255, blank=True, null=True)
    professional_credentials = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Email as the unique login field
    REQUIRED_FIELDS = ['role']  # Only 'role' is required in addition to email

    def __str__(self):
        return f"{self.email} - {self.role}"
