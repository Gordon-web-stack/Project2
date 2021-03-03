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
        List_category = List_category_get,
        List_user = request.user
        )

        Listing.save()
        listing_items = Listings.objects.filter(id = Listing.id)
        return render(request, "auctions/items.html",{
            "items":listing_items
        })

def listing(request, id):
        item = Listings.objects.get(id = id)
        count_item = 0
        count_item = wishlist.objects.filter(user = request.user, item = id ).count()
        bidings = bids.objects.filter(bid_item_id = id)
        if count_item == 0:
            resh = wishlist(item =item , user = request.user)
            resh.save()
            button = "remove from watchlist"
        else:
            wishlist.objects.filter(user = request.user, item = item ).delete()
            button = "Add to watchlist"

        if item.List_user == request.user:
            Listing_poster = True
        else:
            Listing_poster = False
        bid_closed = False
        bid_message=""
        for bid in bidings:
            if bid.bid_won :
                bid_closed = True
                win_user = bid.bid_user
                if request.user == win_user:
                   bid_message = "You won"
                else:
                   bid_message = "bid closed"
            else:
                bid_closed = False
                
        item = Listings.objects.filter(id = id)
        return render(request,"auctions/listing.html",{
        "List": item,
        "count": count_item,
        "button_label":button,
        "listing_poster":Listing_poster,
        "bid_closed":bid_closed,
        
        "bid_message":bid_message
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
    message = ""
    return listing(request,item_id,message)
    
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

def close_bid(request, item_id):
    biddings = bids.objects.filter(bid_item_id = item_id)
    highest_bid = 0
    
    for bid in biddings:
        if bid.bid_amount > highest_bid:
            highest_bid = bid.bid_amount
            highest_bidder = bid.bid_user_id
        

    winning_bid = bids.objects.get(bid_user_id = highest_bidder, bid_item_id = item_id , bid_amount = highest_bid)
    winning_bid.bid_won = True
    winning_bid.save()
    return listing(request,item_id)