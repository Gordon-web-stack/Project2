from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import *



def index(request):
    List_items = Listings.objects.all()

    return render(request, "auctions/index.html",{
        "List" : List_items

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
   return render(request, "auctions/new_listing.html"
   )

def create_listing(request):
    if request.method == "POST":
        List_name = request.POST["item_name"]
        List_description = request.POST["item_description"]
        List_start_price = request.POST["start_price"]
        List_image_url = request.POST["image_url"]

            #DO a check if the listing already exists

        Listing = Listings.objects.create(List_name = List_name, 
        List_description = List_description,
        List_start_price = List_start_price,
        List_image_url = List_image_url,
       
        )

        Listing.save()
        return render(request, "auctions/index.html")

def listing(request, id):
        item = Listings.objects.filter(id = id)
        count_item = 0
        count_item = wishlist.objects.filter(user = request.user, item = id ).count()
        return render(request,"auctions/listing.html",{
        "List": item,
        "count": count_item
        })

def categories(request):
    List_items = Listings.objects.all()
    
    return render(request, "auctions/categories.html",{
        "List" : List_items

    })

def wishlist_add(request,item_id):
    item = Listings.objects.get(id = item_id)
    Listing = Listings.objects.filter(id = item_id)
    count_item = 0
    count_item = wishlist.objects.filter(user = request.user, item = item ).count()
    if count_item == 0:
        resh = wishlist(item =item , user = request.user)
        resh.save()
        button = "remove from wishlist"
    else:
        wishlist.objects.filter(user = request.user, item = item ).delete()
        button = "Add to wishlist"
    
    return render(request,"auctions/listing.html",{
        "count":count_item,
        "List": Listing,
        "button_label":button
        })
    