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
