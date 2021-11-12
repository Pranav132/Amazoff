from django.http import HttpResponse
from products.models import Product, Product_Categories, ReviewsRatings
from django.shortcuts import render, redirect
from .forms import FilterForm
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

# Create your views here.


def index(request):
    # to render the homepage
    return render(request, "index.html")


def cart(request):
    # to render the cart
    return render(request, "cart.html")


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
    # reviews and ratings of the particular product
    # ratings = ReviewsRatings.objects.get(product=product_id)
    return render(request, "product_page.html", {"product": product})


def search(request):

    # search function, using GET method, rendering product_search.html

    if request.method == 'GET':
        search = request.GET['searched']
        product = Product.objects.none()

        print("GET")
        print(search)

        # this gives us all the products who's names are directly related to the search term
        main_product = Product.objects.filter(name__icontains=search)
        related_products = Product.objects.filter(
            category__name__icontains=search)
        far_related_products = Product.objects.filter(
            description__icontains=search)
        product = main_product | related_products | far_related_products

        # initializing the form and setting the default value to be relevance
        form = FilterForm(initial={'name': 'relevance'})
        return render(request, 'product_search.html', {"product": product, "search": search, "form": form})

    if request.method == 'POST':
        form = FilterForm(request.POST)
        search = request.POST.get('searched')

        print("POST")
        print(search)

        main_product = Product.objects.filter(name__icontains=search)
        related_products = Product.objects.filter(
            category__name__icontains=search)
        far_related_products = Product.objects.filter(
            description__icontains=search)
        product = main_product | related_products | far_related_products

        if form.is_valid():
            choice = request.POST.get('name')[0]
            print(choice)

            if choice == 'r':
                product = product

            if choice == 'p':
                product = product.order_by('-popularity')
                print('Popularity')

            if choice == 'l':
                product = product.order_by('price')
                print('Low to High')

            if choice == 'h':
                product = product.order_by('-price')
                print('High to Low')

        return render(request, 'product_search.html', {"product": product, "search": search, "form": form})
