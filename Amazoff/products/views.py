from django.http import HttpResponse, JsonResponse
from products.models import Product, Product_Categories, ReviewsRatings, Addresses, Customer, Cart, CartItem
from django.shortcuts import render, redirect
from .forms import FilterForm
from django.contrib.auth.decorators import login_required
import json
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

# Create your views here.


def index(request):
    # to render the homepage
    return render(request, "index.html")


def cart(request):
    # to render the cart
    cart_id = Cart.objects.get(
        user__username=request.user)
    print(cart_id)

    cart_items = CartItem.objects.filter(cart=cart_id)
    print(cart_items)
    return render(request, "cart.html", {"cart_items": cart_items})


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
    for rating in ratings:
        avg += rating.rating
        count += 1
    if count == 0:
        avg = -1
    else:
        avg = avg / count
        avg = round(avg)
    print(avg)

    return render(request, "product_page.html", {"product": product, "rating": avg})


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    print(customer)
    product = Product.objects.get(id=productId)
    print(product)
    order = Cart.objects.get_or_create(
        user=customer, orderExecuted=False)[0]

    orderItem = CartItem.objects.get_or_create(
        cart=order, product=product)[0]
    print(orderItem)

    if action == 'add':
        orderItem.quant = (orderItem.quant + 1)
    elif action == 'remove':
        orderItem.quant = (orderItem.quant - 1)

    orderItem.save()

    if orderItem.quant <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


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


def contact(request):
    # to render the contact page
    return render(request, "contact.html")


def faq(request):
    # to render the faq page
    return render(request, "faq.html")
