from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class SortingForm(forms.Form):

    # setting the choices users will have to filter search
    CHOICES = [
        ('relevance', 'Relevance'),
        ('popularity', 'Popularity'),
        ('low2high', 'Price: Low to High'),
        ('high2low', 'Price: High to Low')
    ]

    # BRANDS = [
    #     ('ck', 'CK'),
    #     ('creed', 'Creed'),
    #     ('burberry', 'Burberry')
    # ]

    RANGES = [
        ('zero', 'No price filter'),
        ('five', 'Below $500'),
        ('ten', 'Below $1000'),
        ('twenty', 'Below $2000'),
        ('thirty', 'Below $3000'),
        ('fourty', 'Below $4000'),
        ('fifty', 'Below $5000'),
        ('sixty', 'Below $6000'),
        ('seventy', 'Below $7000'),
        ('eighty', 'Below $8000'),
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

    name = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect)

    # brand = forms.MultipleChoiceField(
    #     required=False, widget=forms.CheckboxSelectMultiple, choices=BRANDS)

    price = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect, choices=RANGES)

    gender = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect, choices=GENDERS)

    types = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect, choices=TYPES)

    use = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect, choices=USES)


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
