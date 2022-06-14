from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    CATEGORY = [
    ("Miscellaneous", "Miscellaneous"),
    ("Movies and Television", "Movies and Television"),
    ("Sports", "Sports"),
    ("Arts and Crafts", "Arts and Crafts"),
    ("Clothing", "Clothing"),
    ("Books", "Books"),
]
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    bid = models.DecimalField(max_digits=1000000000000, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    comment = models.CharField(max_length=500)

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    bid = models.DecimalField(max_digits=12, decimal_places=2)

class WatchList(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

class CloseListing(models.Model):
    listings = models.ForeignKey(Listings, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


