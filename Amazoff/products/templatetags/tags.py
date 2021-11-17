from django import template
from ..models import Product, Product_Categories, Tags, subcategories

register = template.Library()


@register.simple_tag
def autocomplete(request):
    products = Product.objects.all()
    categories = Product_Categories.objects.all()
    sub_categories = subcategories.objects.all()
    product_tags = Tags.objects.all()
    return {"products": products, "categories": categories, "subcategories": sub_categories, "tags": product_tags}
