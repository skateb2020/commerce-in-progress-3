from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User, Listings, Comments, Bids, WatchList, CloseListing
from .forms import ListingsForm, CommentForm, BidsForm
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.db.models import Q, Max

def index(request):
    #listings = Listings.objects.exclude(closelisting__listings=listings.all())
    #listings = Listings.objects.all().exclude(id__in=CloseListing)
    #close_listings = CloseListing.objects.all()
    close_listings = CloseListing.objects.values('listings')
    listings=Listings.objects.exclude(id__in=close_listings)
    return render(request, "auctions/index.html",{
        "listings": Listings.objects.all()
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

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        form = ListingsForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
        else:
            return render(request, "auctions/create.html",{
                "form": listing
            })

    form = ListingsForm
    return render(request, "auctions/create.html",{
        "form": form
        })

@login_required(login_url='login')
def watchlist(request):
    listings = Listings.objects.filter(watchlist__user=request.user)
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

@login_required(login_url='login')
def listing(request, id):
    #gets listing
    listing = get_object_or_404(Listings.objects, pk=id)
    #code for comment and bid forms
    listing_price = listing.bid
    sellar = listing.user
    comment_obj = Comments.objects.filter(listing=listing)
    #types of forms
    comment_form = CommentForm()
    bid_form = BidsForm()
    #watchlist_form = WatchListForm()
    #closelisting_form = CloseListingForm()
   
    #close listing code
    if sellar == request.user:
        closeListingButton = True
    else: 
        closeListingButton = False
    closeListing = ''
    try:
        has_closed = get_list_or_404(CloseListing, Q(
            user=request.user) & Q(listings=listing))
    except:
        has_closed = False
    if has_closed:
        closeListing = False
    else: 
        closeListing = True
    
   #watchlist code
    add_or_remove_watchlist = ''
    try:
        has_watchlists = get_object_or_404(WatchList, Q(
            user=request.user) & Q(listing=listing))
        print('--------------------------')
        print(has_watchlists)
        print('--------------------------')
    except:
        has_watchlists = False

    if has_watchlists:
        add_or_remove_watchlist = True
    else:
        print('it will from remove')
        add_or_remove_watchlist = False

    #code for the bid form
    bid_obj = Bids.objects.filter(listing=listing)
    other_bids = bid_obj.all()
    max_bid =0
    for bid in other_bids:
        if bid.bid > max_bid:
            max_bid = bid.bid

    

    #checks if the user can close the listing
    #if sellar == request.user:
        #return render(request, "auctions/listing.html",{
                    #"auction_listing": listing,
                    #"form": comment_form,
                    #"comments": comment_obj,
                    #"bidForm": bid_form,
                    #"bids": bid_obj,
                    #"watchlistForm": watchlist_form, 
                    #"closeListingForm": closelisting_form
                #})
    #else:
        #return render(request, "auctions/listing.html",{
                    #"auction_listing": listing,
                    #"form": comment_form,
                    #"comments": comment_obj,
                    #"bidForm": bid_form,
                    #"bids": bid_obj,
                    #"watchlistForm": watchlist_form
                #})

     #checks if request method is post for all the forms
    if request.method == "POST":
        print(request.POST)
        #forms
        comment_form = CommentForm(request.POST)
        print("POST", request.POST)
        bid_form = BidsForm(request.POST)
        print("FORM", bid_form)
        #closelisting_form = CloseListingForm(request.POST)

        #watchlist code
        if request.POST.get('add'):
            WatchList.objects.create(user=request.user, listing=listing)
            add_or_remove_watchlist = False
        elif request.POST.get('remove'):
            add_or_remove_watchlist = True
            has_watchlists.delete()

        #close listing code
        if request.POST.get('close'):
            CloseListing.objects.create(user=request.user, listings=listing)
            closeListing = True
            closeListingButton = False
            add_or_remove_watchlist = True
            winning_bid = Bids.objects.aggregate(Max('bid'))
            winning_bid = Bids.objects.latest('bid')
            winner = winning_bid.user
            return render(request, "auctions/listing.html",{
                        "auction_listing": listing,
                        "comments": comment_obj,
                        "bids": bid_obj,
                        "closeListingButton": closeListingButton,
                        "closeListing": closeListing,
                        "closedMessage": "This listing is closed.",
                        "winner": winner
            })
        #else:
            #closeListing = False
            #return redirect('listing', id=id)

        #checks if bid form is valid
        if bid_form.is_valid():
            print('!!!!!form is valid')
            #print("bid form is valid")
            new_bid = float(bid_form.cleaned_data.get("bid"))
            if (new_bid >= listing_price) and (new_bid > max_bid):
                bid = bid_form.save(commit=False)
                bid.listing = listing
                bid.user = request.user
                bid.save()
                print("bid form is saving")
            else: 
                print(bid_form.errors)
                print("bid form is not saving")
                return render(request, "auctions/listing.html",{
                    "auction_listing": listing,
                    "form": comment_form,
                    "comments": comment_obj,
                    "bidForm": bid_form,
                    "bids": bid_obj,
                    "message": "Your bid needs to be equal or greater than the listing price and greater than any other bids."
                })
        else:
            print(bid_form.errors, bid_form.non_field_errors)
            print(bid_form.errors)
            return redirect('listing', id=id)

        #watchlist code
        #if request.POST.get('add'):
            #WatchList.objects.create(user=request.user, listing=listing)
            #add_or_remove_watchlist = False
        #elif request.POST.get('remove'):
            #add_or_remove_watchlist = True
            #has_watchlists.delete()

        #close listing code
        #if request.POST.get('close'):
            #CloseListing.objects.create(user=request.user, listings=listing)
            #closeListing = True
            #closeListingButton = False
            #has_watchlists.delete()
            #winner = max_bid.user
            #return render(request, "auctions/listing.html",{
                        #"auction_listing": listing,
                        #"comments": comment_obj,
                        #"bids": bid_obj,
                        #"closeListingButton": closeListingButton,
                        #"closeListing": closeListing,
                        #"closedMessage": "This listing is closed.",
                        #"winner": winner
            #})
        #else:
            #closeListing = False
            #return redirect('listing', id=id)

        #checks if comment form is valid
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
        else:
            return redirect('listing', id=id)

        #what happens if listing is closed
        #if closeListing == True:
            #closeListingButton = False
            #has_watchlists.delete()
            #winner = max_bid.user
            #return render(request, "auctions/listing.html",{
                        #"auction_listing": listing,
                        #"comments": comment_obj,
                        #"bids": bid_obj,
                        #"closeListingButton": closeListingButton,
                        #"closeListing": closeListing,
                        #"closedMessage": "This listing is closed.",
                        #"winner": winner
            #})
        #else: 
            #return redirect('listing', id=id)

        #checks if watchlist form is valid
        #if watchlist_form.is_valid():
            #if watchlist_form.instance.add_to_watchlist == False:
                #watchlist_form.instance.user = request.user
                #watchlist_form.instance.add_to_watchlist = True
                #watchlist = watchlist_form.save()
                #watchlist.listings.add(listing)
                #return render(request, "auctions/listing.html",{
                    #"auction_listing": listing,
                    #"form": comment_form,
                    #"comments": comment_obj,
                    #"bidForm": bid_form,
                    #"bids": bid_obj
                #})
                #return redirect('listing', id=id)
            #else:
                #watchlist_form.instance.user = request.user
                #watchlist_form.instance.add_to_watchlist = False
                #watchlist = watchlist_form.save()
                #watchlist.listings.delete(listing)
                #return redirect('listing', id=id)
            
        #checks if closelisting form is valid
        #if closelisting_form.is_valid():
            #return render(request, "auctions/listing.html",{
                #"auction_listing": listing,
                #"form": comment_form,
                #"comments": comment_obj,
                #"bidForm": bid_form,
                #"bids": bid_obj
            #})
        #return redirect('listing', id=id)
        
       
    return render(request, "auctions/listing.html",{
        "auction_listing": listing,
        "form": comment_form,
        "comments": comment_obj,
        "bidForm": bid_form,
        "bids": bid_obj,
        "watchlist": add_or_remove_watchlist,
        "closeListingButton": closeListingButton, 
        "closeListing": closeListing
    })

def categories(request):
    return render(request, "auctions/categories.html")

def categories_page(request, category):
    listings = Listings.objects.all().filter(category=category)
    return render(request, "auctions/categories_page.html",{
        "listings": listings,
        "heading": category
    })