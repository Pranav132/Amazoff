# In order to pass databse items to the base layout HTML file, we use this file and pass the required variables
# These functions are added to the settings.py file in order to make them accessible on the HTML template

from .models import Wishlist, WishlistItem

# This passes all the items in the wishlist to all pages. This is order to check whether or not a product is
# in a user's wishlist and accordingly change the kind of wishlist icon.


def wishlist_checker(request):

    # initializing dictionary
    wishlistItems = {}

    # we only want the items if the user is logged in, otherwise there is no wishlist to search through
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_Items = WishlistItem.objects.filter(wishlist=wishlist)

        # Setting a key-value pair for all items in the user's wishlist
        for item in wishlist_Items:
            wishlistItems[item.product.name] = True

    return {"template_wishlistItems": wishlistItems}
