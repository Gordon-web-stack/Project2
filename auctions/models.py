from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import time

class User(AbstractUser):
    pass

class category_list(models.Model):
    categories = models.CharField(max_length=128)

class Listings(models.Model):
    List_name = models.CharField(max_length = 32)
    List_description = models.TextField()
    List_start_price = models.FloatField(default=0)
    List_image_url = models.CharField(max_length= 256, blank=True, null=True)
    List_category = models.ForeignKey(category_list,on_delete=models.CASCADE, default = "No Category")
    List_time_made = models.TimeField(auto_now=False, auto_now_add=False, null=True )
    List_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="item_user")

    def __str__(self):
        return f"{self.List_name} ({self.List_description})"

class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_id")
    item = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="item_id")

class bids(models.Model):
    bid_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid_user_id")
    bid_item = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="bid_item_id")
    bid_amount = models.FloatField(default=0)
    bid_won = models.BooleanField(default=False)
