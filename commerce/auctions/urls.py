from django.urls import path
from .models import User, Listings, Comments, Bids, WatchList
from .forms import ListingsForm
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name = "categories"),
    path("categories/<str:category>/", views.categories_page, name = "categories_page"),
    path("listing/<int:id>/", views.listing, name = "listing"),
    path("register", views.register, name="register")
]
