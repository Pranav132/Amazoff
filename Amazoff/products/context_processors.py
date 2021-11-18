from .models import Product, Product_Categories, Tags, subcategories


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
