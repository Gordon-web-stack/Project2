from django.contrib import admin
from .models import *
# Register your models here.

class ListAdmin(admin.ModelAdmin):
    list_display = ("List_name", "List_description")
class CatAdmin(admin.ModelAdmin):
    Category_display = ("categories")
class BidAdmin(admin.ModelAdmin):
    Bid_display = ("bid_user","bid_item","bid_amount")

admin.site.register(Listings, ListAdmin)
admin.site.register(category_list,CatAdmin)
admin.site.register(bids,BidAdmin)

