from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 


class User(AbstractUser):
    pass

CATEGORIES=(
    ('Electronics','electronics'),
    ('Books','books'),
    ('Crafts','crafts'),
    ('Sports','sports')
)

class Bid(models.Model):
    bid_amount=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name="userBid")



class product_details(models.Model):
    name=models.CharField(max_length=64)
    category=models.CharField(max_length=20,choices=CATEGORIES,default="Electronics")
    image = models.ImageField(blank=True,null=True,upload_to='images/')  
    caption=models.CharField(max_length=100)
    geeks_field = models.ForeignKey(Bid, on_delete=models.CASCADE,blank=True,null=True,related_name="bidPrice")
    watchlist = models.ManyToManyField(User,blank=True,null=True,related_name="my_watchlist")
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="owneruser")
    isActive=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Comment_product(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    listing=models.ForeignKey(product_details,on_delete=models.CASCADE,blank=True,null=True,related_name="Listing")
    message=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing }"

