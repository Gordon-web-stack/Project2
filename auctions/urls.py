from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.New_Listing, name="new_listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:id>", views.listing, name="listing" ),
    path("categories", views.categories, name="categories"),
    path("wishlist/<str:item_id>", views.wishlist_add,name="wishlist"),
    path("<str:category_id>", views.find_category, name="find_category"),
    path("make_bid/<str:item_id>", views.make_bid,name="make_bid"),
    path("close_bid/<str:item_id>",views.close_bid,name="close_bid")
]
