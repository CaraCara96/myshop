from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Max, OuterRef, Subquery
from .forms import BidForm, CommentsForm, WatchForm, ListingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import User, Category, Listing, Bid, Comment, WatchList




def index(request):
    if request.user.is_authenticated:
        lst_id = WatchList.objects.filter(user = request.user, active= True).values_list('listing_id', flat=True)
        listing = Listing.objects.filter(active = True).exclude(user=request.user).exclude(id__in=lst_id).order_by('-date')
       
    
    else:
        listing = Listing.objects.filter(active = True)
    
    

    return render(request, "auctions/index.html",{'listing':listing})


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

def categories(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    else:
        category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, "auctions/categories.html", context)

@login_required
def watch_list(request):
    my_list = WatchList.objects.filter(user = request.user , active = True).values_list('listing_id', flat=True)
    listing = Listing.objects.filter(id__in = my_list)
    context = {'listing': listing}
    return render(request, "auctions/watchlist.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        
        if form.is_valid():
            new_item = form.save(commit=False)
            title = form.cleaned_data['title']
            starting_bid = form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']
            picture = form.cleaned_data['picture']
            description = form.cleaned_data['description']

            new_item.user = request.user
            new_item.title = title
            new_item.starting_bid = starting_bid
            new_item.category = category
            new_item.picture = picture
            new_item.description = description

            new_item.save()
            messages.success(request, f"{title} has been added")
            return redirect('my_listing')
        
    else:
        form = ListingForm()

    return render(request, 'auctions/create.html', {'form': form} )


@login_required
def listing(request, list_id):
    list_item = Listing.objects.get(id=list_id)
    results = Bid.objects.filter(listing = list_item ).aggregate(max_amount = Max('amount'))
    current_bid = results['max_amount']
    comments = Comment.objects.filter(listing=list_item).order_by('-date')
    my_bid = Bid.objects.filter(listing = list_item, user = request.user).order_by('-amount').first()
   
    form = BidForm()
    c_form = CommentsForm()
    
   
    context = {"listing": list_item, "current_bid": current_bid, 'form':form, 'c_form': c_form, 'comments': comments, "my_bid":my_bid}

    return render(request, "auctions/listing.html", context)
@login_required
def new_bid(request, bid_item):
    listing = get_object_or_404(Listing, id=bid_item)

    if request.method =='POST':
        form = BidForm(request.POST)
        if form.is_valid():
            amt = float(form.cleaned_data['amount'])

            current_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

            if current_bid is None:
                min_val = listing.starting_bid.amount if hasattr(listing.starting_bid, "amount") else listing.starting_bid
            else:
                min_val = current_bid.amount if hasattr(current_bid, "amount") else current_bid

            if amt > min_val:
                bid = form.save(commit =False)
                bid.listing = listing
                bid.user = request.user
                bid.amt = amt
                bid.save()
                messages.info(request, f"You have placed a bid of: R {amt}")
                return redirect("listing", list_id =listing.id)
          

            else:
                messages.error(request, f"Amount should be higher than the current bid or starting bid. Your Bid: {amt}")
                return redirect("listing", list_id =listing.id)
    else:
        form = BidForm()
    context ={
            'form':form,
            'listing': listing
        }
   
    return render(request, "auctions/listing.html", context)
@login_required
def new_comment(request, comment_id):
    listing = get_object_or_404(Listing, id = comment_id)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            com = form.cleaned_data['comment']
            cmt = form.save(commit= False)
            cmt.listing = listing
            cmt.user = request.user
            cmt.com = com
            cmt.save()
            messages.info(request, f"You have added a new comment")
            return redirect("listing", list_id = listing.id)
        else:
            messages.error(request, "There was an error in your comment")
            return redirect("listing", list_id= listing.id)
        
    else:
        form = CommentsForm()
    context = {
        'c_form': form,
        'listing': listing
    }

    return render(request, "auctions/listing.html", context)
@login_required
def list_item(request, watch_id):
    listing = get_object_or_404(Listing, id = watch_id)
    if request.method == 'POST':
        form = WatchForm(request.POST)
        if form.is_valid():
            active = form.cleaned_data['active']
            watch_item = form.save(commit= False)
            watch_item.listing = listing
            watch_item.user = request.user
            watch_item.active = active
            watch_item.save()
            messages.info(request, f"{listing.title} Added To Your Watch List")
            return redirect("watch_list")
        
    return render(request, "auctions/watchlist.html")
@login_required
def remove_item(request, rem_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, id=rem_id)
        watch_item = WatchList.objects.filter(listing=listing, user=request.user).first()
        
        if watch_item:
            watch_item.active = False
            watch_item.delete()
            messages.error(request, f"{listing.title} Removed From Your Watch List")
            return redirect("watch_list")

    return render(request, "auctions/watchlist.html")
@login_required
def category(request, cat):
   
    listing = Listing.objects.filter(category__name=cat).exclude(user = request.user)
  
    context = {
        'listing': listing
    }

    return render(request, 'auctions/category.html', context)

@login_required  
def my_listing(request):
    user = request.user

   
    highest_bid = Bid.objects.filter(
        listing=OuterRef('pk')
    ).order_by('-amount').values('amount')[:1]

    listings = Listing.objects.filter(user=user, active = True).annotate(
        highest_bid=Subquery(highest_bid)
    ).order_by('-date')

    context = {
        'listings': listings,
    }

    return render(request, "auctions/my_listings.html", context)

@login_required
def update(request, list_id):
    listing = get_object_or_404(Listing, id = list_id)

    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('my_listing')
        
    else:
        form = ListingForm(instance=listing)

    return render(request, "auctions/update.html", {'form': form})
@login_required
def delete(request, list_id):
    listing = get_object_or_404(Listing, id = list_id)

    if request.method == "POST":
        listing.delete()
        return redirect('my_listing')
    
    return render(request, 'auctions/delete.html', {'listing': listing})
@login_required
def close_listing(request, list_id):
    listing = get_object_or_404(Listing, id = list_id, user = request.user)
    if request.method == 'POST':
        
        listing.active = False 
        listing.save()
        messages.success(request, f"{listing.title} has been Closed")
        return redirect("closed_listing")
    return render(request, "auctions/closed.html", {'listing': listing})
@login_required
def closed_listing(request):
    user = request.user

   
    highest_bid = Bid.objects.filter(
        listing=OuterRef('pk')
    ).order_by('-amount').values('amount')[:1]

    listings = Listing.objects.filter(user=user, active = False).annotate(
        highest_bid=Subquery(highest_bid)
    ).order_by('-date')

    context = {
        'listings': listings,
    }

    return render(request, "auctions/closed_listing.html", context)
@login_required
def bids(request):
    user = request.user
    closed_listings = Listing.objects.filter(active = False)
    my_bids = []
    for listing in closed_listings:

        high_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        if high_bid and high_bid.user == user:
            my_bids.append(high_bid)

    context = {
        'my_bids': my_bids
    }
    return render(request, "auctions/bids.html", context)


