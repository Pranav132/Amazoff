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
    wishlist = Wishlist.objects.filter(user=request.user)[0]
    wishlist_Items = WishlistItem.objects.filter(wishlist=wishlist)
    wishlistItems = {}
    for item in wishlist_Items:
        wishlistItems[item.product.name] = True

    return {"template_wishlistItems": wishlistItems}
