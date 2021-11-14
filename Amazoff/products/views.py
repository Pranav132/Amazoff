from django.http import HttpResponse
from products.models import Product, Product_Categories, ReviewsRatings, Addresses, Customer, Cart, User
from django.shortcuts import render, redirect
from .forms import FilterForm
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

# Create your views here.


def index(request):
    # to make every user a customer
    users = User.objects.all()
    for user in users:
        checkCustomer = Customer.objects.filter(user=user).first()
        if not checkCustomer:
            Customer.objects.create(user=user)
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
    # getting average rating of product
    ratings = ReviewsRatings.objects.filter(product=product_id).all()
    avg = 0.0
    count = 0
    stars = [-1, -1, -1, -1, -1]
    for rating in ratings:
        avg += rating.rating
        count += 1
    if count == 0:
        avg = -1
    else:
        avg = avg / count
        avg = round(avg)
        for i in range(avg):
            stars[i] = 0
    print(stars)

    return render(request, "product_page.html", {"product": product, "rating": stars, "ratingsCount": count})


def user(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    print(customer)
    addresses = Addresses.objects.filter(Customer=customer).all()
    print(addresses)
    print(user.first_name)
    orderHistory = Cart.objects.filter(
        user=user, orderExecuted=True).all()
    print(orderHistory)
    reviews = ReviewsRatings.objects.filter(user=user).all()
    print(reviews)
    cart = Cart.objects.filter(user=user, orderExecuted=False).first()
    print(cart)
    return render(request, "user.html", {"user": user, "addresses": addresses, "orderHistory": orderHistory, "cart": cart, "reviews": reviews})


def order(request, cart_id):
    pass


def review(request, product_id):
    ratings = ReviewsRatings.objects.filter(product=product_id).all()
    for rating in ratings:
        print(rating.user, rating.product, rating.rating, rating.review)

    return render(request, "reviews.html", {"ratings": ratings})


def search(request):

    # search function, using GET method, rendering product_search.html

    if request.method == 'GET':
        search = request.GET['searched']
        product = Product.objects.none()

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

        main_product = Product.objects.filter(name__icontains=search)
        related_products = Product.objects.filter(
            category__name__icontains=search)
        far_related_products = Product.objects.filter(
            description__icontains=search)
        product = main_product | related_products | far_related_products

        if form.is_valid():
            choice = request.POST.get('name')

            if choice == 'relevance':
                product = product

            if choice == 'popularity':
                product = product.order_by('-popularity')

            if choice == 'low2high':
                product = product.order_by('price')

            if choice == 'high2low':
                product = product.order_by('-price')

        return render(request, 'product_search.html', {"product": product, "search": search, "form": form})
