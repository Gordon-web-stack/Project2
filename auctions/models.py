from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import time

class User(AbstractUser):
    pass

class categories(models.Model):
    category = models.CharField(max_length=128)
    
class Listings(models.Model):
    List_name = models.CharField(max_length = 32)
    List_description = models.TextField()
    List_start_price = models.FloatField(default=0)
    List_image_url = models.CharField(max_length= 256, blank=True, null=True)
    List_time_made = models.TimeField(auto_now=False, auto_now_add=False, null=True )
    List_category  = models.ForeignKey(categories,on_delete=models.CASCADE,related_name="item_category",default = "No Category")

    def __str__(self):
        return f"{self.List_name} ({self.List_description})"

class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_id")
    item = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="item_id")


    