from django.http import HttpResponse, JsonResponse
from products.models import Product, Product_Categories, ReviewsRatings, Addresses, Customer, Cart, CartItem, User
from django.shortcuts import render, redirect
from .forms import FilterForm, newAddressForm, ReviewForm
from django.contrib.auth.decorators import login_required
import json
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
        checkCart = Cart.objects.filter(user=user)
        if not checkCart:
            Cart.objects.create(user=user)
    # to render the homepage
    return render(request, "index.html")


def cart(request):
    # to render the cart
    print(request.user)
    cart_id = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart_id)
    return render(request, "cart.html", {"cart_items": cart_items})


def products(request):

    # rendering every required product

    # in this case, rendering all products
    products = Product.objects.all()
    prods = []
    # parsing through returned product objects and creating nested lists with required values

    for product in products:
        prods.append([product.picture1, product.id, product.name, product.price,
                      product.description, product.popularity, product.inventory])

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
    addresses = Addresses.objects.filter(customer=customer).all()
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
    user = request.user
    ratings = ReviewsRatings.objects.filter(product=product_id).all()
    product = Product.objects.filter(id=product_id)[0]
    prod_id = product_id
    checker = [0, 0, 0, 0, 0]
    return render(request, "reviews.html", {"ratings": ratings, "checker": checker, "product_id": prod_id, "user": user, "product": product})


def deleteReview(request, reviewsRatings_id):
    review = ReviewsRatings.objects.filter(id=reviewsRatings_id)
    print(review)
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.filter(id=product_id)
        review.delete()
        return redirect('review', product_id=product_id)


def orderHistory(request):
    orders = Cart.objects.filter(user=request.user, orderExecuted=True).all()
    for order in orders:
        print(order.cartValue)
        print(order.orderDate)
    # prints the order history of the current customer


def newReview(request, product_id):
    # importing all existing reviews and ratings
    # review form
    if request.method == 'GET':
        form = ReviewForm(initial={"rating": 5})
        return render(request, "new_review.html", {"form": form, "product_id": product_id})

    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(id=product_id)
        new_review = ReviewsRatings.objects.create(user=user, product=product)
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            new_review.rating = rating
            new_review.review = review

            new_review.save()

            return redirect('review', product_id=product_id)

    # create review form for user to fill - GET
    # send data back and make a new review and rating in database - POST
    # rating is required but review is not
    # use the same input number from 1 to 5 for review


def search(request):

    # search function, using GET method, rendering product_search.html

    if request.method == 'GET':
        search = request.GET['searched']
        product = Product.objects.none()

        # this gives us all the products who's names are directly related to the search term
        main_product = Product.objects.filter(name__icontains=search)
        product_categories = Product.objects.filter(
            category__name__icontains=search)
        product_subcategories = Product.objects.filter(
            sub_categories__name__icontains=search)
        product_tags = Product.objects.filter(
            tags__name__icontains=search)
        product_descriptions = Product.objects.filter(
            description__icontains=search)
        product = main_product | product_categories | product_subcategories | product_tags | product_descriptions

        # initializing the form and setting the default value to be relevance
        form = FilterForm(initial={'name': 'relevance'})
        return render(request, 'product_search.html', {"product": product, "search": search, "form": form})

    if request.method == 'POST':
        form = FilterForm(request.POST)
        search = request.POST.get('searched')

        main_product = Product.objects.filter(name__icontains=search)
        product_categories = Product.objects.filter(
            category__name__icontains=search)
        product_subcategories = Product.objects.filter(
            sub_categories__name__icontains=search)
        product_tags = Product.objects.filter(
            tags__name__icontains=search)
        product_descriptions = Product.objects.filter(
            description__icontains=search)
        product = main_product | product_categories | product_subcategories | product_tags | product_descriptions

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


@login_required
def checkout(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    current_cart = Cart.objects.get(user=user, orderExecuted=False)
    cart_items = CartItem.objects.filter(cart=current_cart.id)
    print(cart_items)
    user_name = user.first_name
    user_addresses = Addresses.objects.filter(customer=customer).all()
    print(user)
    print(user_addresses)

    if request.method == 'POST':
        price_quant_totals = []
        # quant_totals = []
        outofstock = []
        for product in cart_items:
            # for every item of the cart, take the passed quantity
            quantity = request.POST.get(product.product.name)
            quantity = int(quantity)
            # then change quantity of cart item to that quantity
            product.quant = quantity

            if product.quant == 0:
                print('DELETE')
                product.delete()
            else:
                print('SAVING...')
                # quantity requested is non-zero
                # checking if it is lesser than product inventory
                inventory = product.product.inventory
                if product.quant <= inventory:
                    product.save()
                    price_quant_totals.append(
                        [product.product.name, product.product.price * product.quant, product.quant])
                    # price_totals[product.product.name] = (
                    #     product.quant * product.product.price)
                    # quant_totals.append([product.product.name, product.quant])
                else:
                    # if not enough stock left, send an alert about stock and fix quant to max available
                    print('Not enough products, setting quantity to max avaiable')
                    outofstock.append(product.product.name)
                    product.quant = inventory
                    product.save()
                    price_quant_totals.append(
                        [product.product.name, product.product.price * product.quant, product.quant])
                    # price_totals[product.product.name] = (
                    #     product.quant * product.product.price)
                    # quant_totals.append([product.product.name, product.quant])
                    # quant_totals[product.product.name] = product.quant

        # calculate the value and send to html page
        total_price = 0
        total_quant = 0
        for product in price_quant_totals:
            total_price = product[1] + total_price
            total_quant = product[2] + total_quant

        print(total_price)
        print(total_quant)
        print(price_quant_totals)
        print(outofstock)

    return render(request, "checkout.html", {"user": user, "price_quant_totals": price_quant_totals, "total_price": total_price, "total_quant": total_quant, "outofstock": outofstock, "user_addresses": user_addresses})

    return HttpResponse("There seems to have been an error. Didn't account for you being an absolute moron")


def newAddress(request):
    cart = Cart.objects.get(user=request.user)

    if request.method == 'GET':
        form = newAddressForm()
        return render(request, 'new_address.html', {"form": form})

    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        name = request.POST.get('name')
        addressLine1 = request.POST.get('addressLine1')
        addressLine2 = request.POST.get('addressLine2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipCode = request.POST.get('zipCode')
        user_addresses = Addresses.objects.create(customer=customer, name=name, addressLine1=addressLine1,
                                                  addressLine2=addressLine2, city=city, state=state, country=country, zipCode=zipCode)
        print(user_addresses)
        return HttpResponse("<h1>Yes</h1>")
