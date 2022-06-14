from django.contrib import admin
from auctions.models import WatchList
from auctions.models import CloseListing
# Register your models here.
from .models import Listings, Comments, Bids, WatchList, CloseListing

admin.site.register(Listings)

admin.site.register(Comments)

admin.site.register(Bids)

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'user']

@admin.register(CloseListing)
class CloseListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listings', 'user']

#admin.site.register(CloseListing)