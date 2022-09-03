from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

#name -> name of the product
def itempage(request, name):
    if request.method == "POST":
        #If user is not signed in redirect to login
        if request.POST.get('signin') is not None:
            return render(request, "auctions/login.html")

        #if user clicked watchlist button 
        if request.POST.get('watchlist') is not None:
            item = Watchlist(user=request.user, item=Item.objects.get(title=name))
            item.save()
            return render(request, "auctions/itempage.html", {
                   "item": Item.objects.get(title=name),
                   "user": request.user,
                   "message": "Item Added to watchlist!",
                   "color": "success",
                   "included": "included" 
                })
        
        #if user clicked removewatchlist button
        if request.POST.get('removewatchlist') is not None:
            item = Watchlist.objects.filter(user=request.user, item=Item.objects.get(title=name))
            if item:
                item.delete()
                return render(request, "auctions/itempage.html", {
                   "item": Item.objects.get(title=name),
                   "user": request.user,
                   "message": "Removed Successfully!",
                   "color": "danger"
                })
        
        #if user clicked placebid button
        if request.POST.get('placebid') is not None:
            item = Item.objects.get(title=name)
            newBid = int(request.POST['bid'])
            
            #if new Bid is greater than bid 
            if (newBid > item.bid):
                #updating item 
                item.bid = newBid
                item.lastBidder = request.user
                item.save()
                return render(request, "auctions/itempage.html", {
                        "item": Item.objects.get(title=name),
                        "user": request.user,
                        "message": "Bidding amount is updated!",
                        "color":"success"
                    })
            else:
                return render(request, "auctions/itempage.html", {
                        "item": Item.objects.get(title=name),
                        "user": request.user,
                        "message": "Bidding amount cannot be less than minimum!",
                        "color": "danger"
                    })

        #if closebid is clicked 
        if request.POST.get('closebid') is not None:
            #updating the item object
            item = Item.objects.get(title=name)
            item.isActive = False
            item.owner_id = item.lastBidder
            item.save()
            return render(request, "auctions/itempage.html", {
                        "item": Item.objects.get(title=name),
                        "user": request.user,
                        "message": f"Bid has been awarded to {item.lastBidder.username} for ${item.bid}",
                        "color":"success"
                    })

        #if comment is clicked 
        if request.POST.get('comment') is not None:
            comment = request.POST["commentbox"]
            item = Item.objects.get(title=name)
            commentObject = Comments(item=item, user=request.user, comment=comment)
            commentObject.save()
            comments = Comments.objects.filter(item=item)
            return render(request, "auctions/itempage.html", {
                        "item": Item.objects.get(title=name),
                        "user": request.user,
                        "comments": comments,
                        "message": "Comment Posted Successfully",
                        "color":"success"
                    })

    else:
        #Renders itempage
        items = Item.objects.filter(title=name)
        if items:
            comments = Comments.objects.filter(item=items[0])
            return render(request, "auctions/itempage.html", {
                    "item" : items[0],
                    "user" : request.user,
                    "comments" : comments
                })
        else:
            return render(request, "auctions/error.html", {
                "message":"Page not found!"
            })
        

def index(request):

    # Getting all objects
    items = Item.objects.all()
    watchlist = Watchlist.objects.all()

    # Handling post request
    if request.method == "POST":
        for item in items:
            #if that item is clicked 
            if request.POST.get(item.title) is not None:
                #loading all the comments
                comments = Comments.objects.filter(item=item)

                #checking if in watchlist
                for element in watchlist:
                    if item.id == element.item.id:
                        return render(request, "auctions/itempage.html", {
                        "item" : item,
                        "user" : request.user,
                        "comments" : comments,
                        "included": "included"
                        })
                        
                #render normal if not in watchlist
                return render(request, "auctions/itempage.html", {
                    "item" : item,
                    "user" : request.user,
                    "comments" : comments
                })
    else:
        return render(request, "auctions/index.html", {
            "items" : items,
            "user" : request.user
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

def createlisting(request):
    if request.method == "POST":
        #Taking required Input 
        title = request.POST["title"]
        bid = request.POST["bid"]
        description = request.POST["description"]
        image = request.POST["url"]
        category = Categories.objects.get(id = int(request.POST["category"]))
        
        #creating item object and saving in database
        item = Item(title=title, bid=bid, description=description, image=image, owner_id=request.user, category=category)
        item.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listings.html", {
            "categories": Categories.objects.all()
        })

def watchlist(request):
    #items that user is watching
    items = Watchlist.objects.all()
    watchlist = []

    #Filtering specific user's watchlist
    for item in items:
        if item.user.id == request.user.id:
            watchlist.append(item.item)

    if request.method == "POST":
        for item in watchlist:
            #if that item is clicked 
            if request.POST.get(item.title) is not None:
                #Since item is already in watchlist, render directly
                return render(request, "auctions/itempage.html", {
                    "item" : item,
                    "user" : request.user,
                    "included": "included"
                })     
    else:
        return render(request, "auctions/watchlist.html", {
            "items": watchlist
        })
 
def category(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def display_category(request, category):
    item = Item.objects.filter(category = Categories.objects.get(category=category).id)
    return render(request, "auctions/category.html", {
        "items": item
    })

