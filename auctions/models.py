
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Category")

    def __str__(self):
        return self.name

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    date = models.DateTimeField(verbose_name="Listing Date", default=timezone.now)
    title = models.CharField(max_length=25, verbose_name="Listing Title",unique=True)
    starting_bid = models.FloatField(verbose_name="Listing Starting Bid")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,  verbose_name="Listing Category")
    picture = models.URLField(blank=True, null=True, verbose_name="Listing Image")
    description = models.CharField(max_length=200, verbose_name="Listing Description")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Listing")
    amount = models.FloatField(verbose_name="Bid Amount")
    status = models.BooleanField(default=False, verbose_name="Bid Status")


    def __str__(self):
        return f"{self.user.username} bid on {self.listing.title}: ${self.amount} "

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Listing")
    comment = models.CharField(max_length=200, verbose_name="Comment")
    date = models.DateTimeField(verbose_name="Comment Date", default=timezone.now)

    def __str__(self):
        return self.comment
    

class WatchList(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Listing")
     active = models.BooleanField(default=False, verbose_name="Watch List Status")

     def __str__(self):
        return f"{self.user.username}'s watch list item: {self.listing.title}"

