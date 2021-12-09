# This file contains all forms used in the web app

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


# Form for all the sorting and filtering options on product page and search page
class FilterForm(forms.Form):

    # Setting choices for users to choose from for each kind of input

    CHOICES = [
        ('relevance', 'Relevance'),
        ('popularity', 'Popularity'),
        ('low2high', 'Price: Low to High'),
        ('high2low', 'Price: High to Low')
    ]

    RANGES = [
        ('zero', 'No price filter'),
        ('five', 'Below ₹500'),
        ('ten', 'Below ₹1000'),
        ('twenty', 'Below ₹2000'),
        ('thirty', 'Below ₹3000'),
        ('fourty', 'Below ₹4000'),
        ('fifty', 'Below ₹5000'),
        ('sixty', 'Below ₹6000'),
        ('seventy', 'Below ₹7000'),
        ('eighty', 'Below ₹8000'),
    ]

    GENDERS = [
        ('none', 'No gender filter'),
        ('men', 'Men'),
        ('women', 'Women')
    ]

    TYPES = [
        ('nothing', 'No type filter'),
        ('toilette', 'Eau de Toilette'),
        ('parfum', 'Eau de Parfum'),
        ('misc', 'Other'),
    ]

    USES = [
        ('useless', 'No use filter'),
        ('everyday', 'Everyday'),
        ('nightlife', 'Nightlife'),
        ('sporty', 'Sporty'),
    ]

    # Setting inputs and types of inputs

    name = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(
            attrs={'class': 'dropdown-item'}
        ))

    price = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=RANGES)

    gender = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=GENDERS)

    types = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=TYPES)

    use = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=USES)


# Form for collecting new addresses from users
class newAddressForm (forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Name", widget=forms.TextInput(
        attrs={'placeholder': 'Name of Address',
               'class': 'form-control'}))
    addressLine1 = forms.CharField(max_length=100, label="Address Line 1", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Address Line 1',
               'class': 'form-control'}))
    addressLine2 = forms.CharField(max_length=100, required=False, label='Address Line 2', widget=forms.TextInput(
        attrs={'placeholder': 'Address Line 2',
               'class': 'form-control'}))
    city = forms.CharField(max_length=100, label='City', widget=forms.TextInput(
        attrs={'placeholder': 'City',
               'class': 'form-control'}))
    state = forms.CharField(max_length=100, label='State', widget=forms.TextInput(
        attrs={'placeholder': 'State',
               'class': 'form-control'}))
    country = forms.CharField(max_length=100, label='Country', widget=forms.TextInput(
        attrs={'placeholder': 'Country',
               'class': 'form-control'}))


# Form for collecting reviews from users
class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Rating', widget=forms.NumberInput(
        attrs={'min': 1, 'max': '5', 'type': 'number',
               'class': 'form-control'}))
    review = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Tell us what you think!',
               'class': 'form-control'}))
