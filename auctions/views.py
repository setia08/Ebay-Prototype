from itertools import product
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Bid, User,product_details,Comment_product
from django.forms import ModelForm
from django.shortcuts import redirect

from django.db import models

CATEGORIES=(
    ('Electronics','electronics'),
    ('Books','books'),
    ('Crafts','crafts'),
    ('Sports','sports')
)

class products_details_form(ModelForm):
    name=forms.CharField(max_length=64)
    image = forms.ImageField()  
    caption=forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':20}))
    price  = forms.IntegerField(min_value=0)
    category= forms.CharField(label='category', widget=forms.Select(choices=CATEGORIES))

    class Meta:
        model=product_details
        fields=['name','image','caption','geeks_field','category']



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        products =product_details.objects.all()
        return render(request, "auctions/index.html",{
            "products":products
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


def product_form(request):
    if request.method=="POST":
        price=request.POST.get('price')
        current_user=request.user
        bid=Bid(bid_amount=int(price),user=current_user)
        bid.save()
        form=product_details()
        current_user=request.user
        form.name=request.POST.get('name')
        form.category =request.POST.get('category')
     #   form.image =request.POST.get('image')
        form.image=request.FILES['upload']
        form.caption =request.POST.get('caption')
        form.geeks_field =bid
        form.owner=current_user
        form.save()
        return redirect(index)
    return render(request,'auctions/details.html',{
            "Details":products_details_form
        })

def product_detail(request,id):
    product=product_details.objects.get(pk=id)
    ListinginwatchList=request.user in product.watchlist.all()
    allComments=Comment_product.objects.filter(listing=product)
    isOwner=request.user==product.owner
    current_bid=product.geeks_field.bid_amount
    return render(request,"auctions/view.html",{"product":product,"ListinginwatchList":ListinginwatchList,
    "allcomments":allComments,"current_bid":current_bid,"isOwner":isOwner})


def addtowatchList(request,id):
        product=product_details.objects.get(pk=id)
        currentuser=request.user
        product.watchlist.add(currentuser)
        return HttpResponseRedirect(reverse("index"))

def removefromwatchList(request,id):
        product=product_details.objects.get(pk=id)
        currentuser=request.user
        product.watchlist.remove(currentuser)
        return HttpResponseRedirect(reverse("index"))

def myListing(request):
    id=request.user.id
    print("my",id)
    products =product_details.objects.filter(owner=id)
    print(products)
    return render(request,'auctions/myListing.html',{
        "products":products
    })

def categories(request,my_category):
    category=my_category.capitalize()
    cats =product_details.objects.filter(category=category)
    return render(request,'auctions/category.html',{
        "products":cats,
        "categories":category
    })

def allcategories(request):
    return render(request,"auctions/myCategory.html")


def viewwatchList(request):
    watchlist_list = request.user.my_watchlist.all()
    return render (request,"auctions/watchList.html",{
        "watchlist_lists":watchlist_list
    })

def add_comment(request,id):
    currentuser=request.user
    currentproduct=product_details.objects.get(pk=id)
    message_given=request.POST['newcomment']
    new_Comment= Comment_product(
        author=currentuser,
        listing=currentproduct,
        message=message_given
    )
    new_Comment.save()
    return HttpResponseRedirect(reverse("product_details",args=(id,)))


def place_bid(request,id):
    currentproduct=product_details.objects.get(pk=id)
    latest_bid_amount=int(request.POST["bid"])
    current_bid=currentproduct.geeks_field.bid_amount
    if latest_bid_amount<current_bid:
        return render(request,"auctions/view.html",{
        "current_bid":current_bid,
        "product":currentproduct,
        "message":"Bid was Failed",
        "update":False
        })
    else:
        updateBid=Bid(user=request.user,bid_amount=latest_bid_amount)
        updateBid.save()
        currentproduct.geeks_field=updateBid
        currentproduct.save()        
        return render(request,"auctions/view.html",{
            "current_bid":current_bid,
            "product":currentproduct,
       "message":"Bid was successful",
       "update":True
        })

def close_bid(request,id):
    currentproduct=product_details.objects.get(pk=id)
    current =currentproduct.owner
    currentuser=request.user
    currentproduct.isActive=False
    currentproduct.save()
    return render(request,"auctions/view.html",{
        "product":currentproduct,
        "current":current,
        "currentuser":currentuser
    })

