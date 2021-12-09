from .models import Product, Product_Categories, Tags, subcategories, Wishlist, WishlistItem, Cart


def autocomplete_processor(request):

    if request.user:
        print(request.user)

        cart = Cart.objects.filter(user=request.user, orderExecuted=False).first()
        if cart:
            cart_items = cart.calcCartQuant
        else:
            cart_items = 0

    products = Product.objects.all()
    categories = Product_Categories.objects.all()
    sub_categories = subcategories.objects.all()
    product_tags = Tags.objects.all()
    return {
        "cart_len":cart_items,
        "template_products": products,
        "template_categories": categories,
        "template_subcategories": sub_categories,
        "template_tags": product_tags
    }


def wishlist_checker(request):
    wishlistItems = {}
    # print(request.user)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        # print(wishlist.user)
        # print(wishlist.id)
        wishlist_Items = WishlistItem.objects.filter(wishlist=wishlist)
        # print(wishlist_Items)
        for item in wishlist_Items:
            wishlistItems[item.product.name] = True

    return {"template_wishlistItems": wishlistItems}
