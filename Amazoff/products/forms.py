from django import forms


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
    addressLine1 = forms.CharField()
    addressLine2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    zipCode = forms.IntegerField()
