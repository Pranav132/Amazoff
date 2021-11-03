from django.http import HttpResponse
from products.models import Product, Product_Categories, ReviewsRatings
from django.shortcuts import render, redirect
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

# Create your views here.


def index(request):
    # to render the homepage
    return render(request, "index.html")


def products(request):

    # rendering every required product

    # in this case, rendering all products
    products = Product.objects.all()
    prods = []
    # parsing through returned product objects and creating nested lists with required values

    for product in products:
        prods.append([product.picture1, product.id, product.name, product.site_title, product.price,
                      product.description, product.popularity])

    # sending to products.html file
    return render(request, "products.html", {"products": products})


def product(request, product_id):
    # specific product page, accessing data of each product through product ID primary key
    product = Product.objects.get(id=product_id)
    return render(request, "product_page.html", {"product": product})


def search(request):

    # search function, using POST method, rendering product_search.html

    if request.method == 'POST':
        search = request.POST['searched']
        all_products = Product.objects.all()

        product = Product.objects.filter(name__icontains=search)

        return render(request, 'product_search.html', {"product": product, "search": search})
