from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    List_name = models.CharField(max_length = 32)
    List_description = models.TextField()
    List_start_price = models.FloatField(default=0)
    List_image_url = models.CharField(max_length= 64, null=True)
    
    def __str__(self):
        return f"{self.List_name} ({self.List_description})"
