from django.contrib.auth.models import AbstractUser
from django.db import models
 
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        SHOP_OWNER = "SHOP_OWNER", "Shop owner"
        RIDER = "RIDER", "Dispatch rider"
        ADMIN = "ADMIN", "Administrator"
 
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]
 
    def __str__(self):
        return f"{self.email} ({self.role})"
