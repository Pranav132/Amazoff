from django.contrib import admin
from .models import Product, ReviewsRatings, User


# Register your models here.
admin.site.register(Product)
admin.site.register(ReviewsRatings)
admin.site.register(User)
