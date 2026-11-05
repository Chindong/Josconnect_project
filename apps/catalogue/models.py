from django.db import models
from apps.shops.models import ShopProfile
 
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
 
    def __str__(self):
        return self.name
 
class Product(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["name"]
 
    def __str__(self):
        return f"{self.name} - {self.shop.name}"
