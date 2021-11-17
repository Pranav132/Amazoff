from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class FilterForm(forms.Form):

    # setting the choices users will have to filter search
    CHOICES = [
        ('relevance', 'Relevance'),
        ('popularity', 'Popularity'),
        ('low2high', 'Price: Low to High'),
        ('high2low', 'Price: High to Low')
    ]

    name = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect)


class newAddressForm (forms.Form):
    name = forms.CharField(max_length=100, required=True)
    addressLine1 = forms.CharField(max_length=100)
    addressLine2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)


class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Rating', widget=forms.NumberInput(
        attrs={'min': 1, 'max': '5', 'type': 'number'}))
    review = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Tell us what you think!'}))
