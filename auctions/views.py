from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import ConnectionDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
import datetime
from .models import *

def index(request):
    List_items = Listings.objects.all()

    return render(request, "auctions/items.html",{
        "items" : List_items,
        "heading": "Active Listing"

    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def New_Listing(request):
    Category_list = category_list.objects.all()
    return render(request, "auctions/new_listing.html",{
        "categories":Category_list
    }
    )

def create_listing(request):
    if request.method == "POST":
        List_name = request.POST["item_name"]
        List_description = request.POST["item_description"]
        List_start_price = request.POST["start_price"]
        List_image_url = request.POST["image_url"]
        List_category = request.POST["category_list"]
        List_category_get = category_list.objects.get(id = List_category)

            #DO a check if the listing already exists

        Listing = Listings.objects.create(
        List_name = List_name, 
        List_description = List_description,
        List_start_price = List_start_price,
        List_image_url = List_image_url,
        List_category = List_category_get
       
        )

        Listing.save()
        listing_items = Listings.objects.filter(id = Listing.id)
        return render(request, "auctions/items.html",{
            "items":listing_items
        })

def listing(request, id):
        item = Listings.objects.filter(id = id)
        count_item = 0
        count_item = wishlist.objects.filter(user = request.user, item = id ).count()
        button = "Add to watchlist"
        return render(request,"auctions/listing.html",{
        "List": item,
        "count": count_item,
        "button_label":button
        })

def categories(request):
    All_categories = category_list.objects.all()
    
    return render(request, "auctions/categories.html",{
        "categories":All_categories

    })

def find_category(request,category_id):
    item_list = Listings.objects.filter(List_category_id = category_id)
    category_name = category_list.objects.get(id = category_id).categories
    
    return render(request, "auctions/items.html",{
        "items":item_list,
        "title": category_name,
        "heading":"category : " + category_name
    })

def wishlist_add(request,item_id):
    item = Listings.objects.get(id = item_id)
    Listing = Listings.objects.filter(id = item_id)
    count_item = 0
    count_item = wishlist.objects.filter(user = request.user, item = item ).count()
    if count_item == 0:
        resh = wishlist(item =item , user = request.user)
        resh.save()
        button = "remove from watchlist"
    else:
        wishlist.objects.filter(user = request.user, item = item ).delete()
        button = "Add to watchlist"
    
    return render(request,"auctions/listing.html",{
        "count":count_item,
        "List": Listing,
        "button_label":button
        })
    
def make_bid(request,item_id):
    new_bid_amount = request.POST["bid_amount"]
    list_item = Listings.objects.get(id = item_id)
    item = list_item
    list_item = Listings.objects.filter(id = item_id)
    message=" "
    
    if bids.objects.filter(bid_item_id = item.id).exists():
       
        Largest_bid = 0
        current_bids = bids.objects.filter(bid_item_id = item_id)
        for bid in current_bids:
            if float(bid.bid_amount) > Largest_bid:
                Largest_bid = float(bid.bid_amount)

        if float(new_bid_amount) > Largest_bid:
            new_bid = bids.objects.create(bid_user = request.user, bid_amount = new_bid_amount, bid_item = item )
            new_bid.save() 
        else:
            message = "Bid must be larger than all current bids"
    else:
        current_bids = item.List_start_price
        if float(new_bid_amount) >= float(item.List_start_price):
            new_bid = bids.objects.create(bid_user = request.user, bid_amount = new_bid_amount, bid_item = item )
            new_bid.save() 
        else:
            message="Bid must be larger than or equal to starting price"

    return render(request,"auctions/listing.html",{
        "List":list_item,
        "message":message
    } )
            