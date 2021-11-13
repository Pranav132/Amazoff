from django.contrib import admin
from .models import Tags, Customer, Product, ReviewsRatings, User, Product_Categories, Cart, CartItem, Wishlist, WishlistItem, subcategories, Addresses


# Register your models here.
admin.site.register(Product)
admin.site.register(ReviewsRatings)
admin.site.register(Product_Categories)
admin.site.register(subcategories)
admin.site.register(Customer)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Addresses)
admin.site.register(WishlistItem)
admin.site.register(Tags)
