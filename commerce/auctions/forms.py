from django import forms
from .models import Listings, Comments, Bids
from django.forms.widgets import HiddenInput

class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'bid', 'image', 'category']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'Add the title of your listing here.', 'class' : 'form-control'}),
                   'description': forms.TextInput(attrs={'placeholder': 'Add a description of your listing here.', 'class' : 'form-control'}),
                   'bid': forms.NumberInput(attrs={'placeholder': 'Add a starting price for your listing here.', 'class' : 'form-control', 'style': 'height: 125%;'}),
                   'image': forms.TextInput(attrs={'placeholder': 'Add an optional url of your product here.', 'class' : 'form-control', 'style': 'height: 125%;'})
        }
     
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {'comment': forms.TextInput(attrs={'placeholder': 'Add a comment about this listing here.', 'class' : 'form-control'})}

class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid']
        widgets = {'title': forms.NumberInput(attrs={'placeholder': 'Add a bid for this listing here.', 'class' : 'form-control'})}
