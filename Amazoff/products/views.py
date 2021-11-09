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
        prods.append([product.picture1, product.id, product.name, product.price,
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
        product = Product.objects.none()

        # this gives us all the products who's names are directly related to the search term
        main_product = Product.objects.filter(name__icontains=search)
        related_products = Product.objects.filter(
            category__name__icontains=search)
        product = main_product | related_products

        # from the search term, find the product category that fits with that.

        # searched_category = Product_Categories.objects.filter(
        #     name__icontains=search)

        # # get the id of that category and filter all products with that ID

        # category_ID = []

        # for category in searched_category:
        #     category_ID.append(category.id)

        # for category_id in category_ID:
        #     related_products = Product.objects.filter(
        #         category__icontains=category_id)

        #     product = related_products | product

        return render(request, 'product_search.html', {"product": product, "search": search})
