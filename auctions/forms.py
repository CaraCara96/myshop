from django import forms
from .models import Bid, Comment, WatchList, Listing

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount'] 
        widgets = {
            'amount': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Place Your Bid'})
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Add Your Comment', 'rows':'3', 'id': 'exampleFormControlTextarea1'})
        }

class WatchForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ['active']

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ['title', 'starting_bid','category','picture', 'description']
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Listing Title'}),
            'starting_bid':forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Place Your Starting Bid'}),
            'category':forms.Select(attrs={'class': 'form-control', 'placeholder':'Listing Category'}),
            'picture':forms.URLInput(attrs={'class': 'form-control', 'placeholder':'Enter Your Image URL'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Type Your Description', 'rows':'3', 'id': 'exampleFormControlTextarea1'})

        }

        