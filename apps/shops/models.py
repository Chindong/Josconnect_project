from django.conf import settings
from django.db import models
from django.utils.text import slugify
 
class ShopProfile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 related_name="shop_profile")
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
 
    def __str__(self):
        return self.name
