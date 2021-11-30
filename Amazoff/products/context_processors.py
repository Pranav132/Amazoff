from .models import Product, Product_Categories, Tags, subcategories, Wishlist, WishlistItem


def autocomplete_processor(request):
    products = Product.objects.all()
    categories = Product_Categories.objects.all()
    sub_categories = subcategories.objects.all()
    product_tags = Tags.objects.all()
    return {
        "template_products": products,
        "template_categories": categories,
        "template_subcategories": sub_categories,
        "template_tags": product_tags
    }


def wishlist_checker(request):
    wishlistItems = {}
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_Items = WishlistItem.objects.filter(wishlist=wishlist)
        for item in wishlist_Items:
            if item.product:
                wishlistItems[item.product.name] = True

    return {"template_wishlistItems": wishlistItems}
