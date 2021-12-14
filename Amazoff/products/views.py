from django.http import HttpResponse, JsonResponse
from .models import Product, Product_Categories, Tags, ReviewsRatings, Addresses, Customer, Cart, CartItem, User, Wishlist, WishlistItem, completedOrders, subcategories
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q


# Create your views here.


def index(request):
    # to make every user a customer
    users = User.objects.all()
    for user in users:

        # This all checks if the users in the database have a customer, cart and wishlist associated with them
        # If they don't, this creates one and assigns it to them

        checkCustomer = Customer.objects.filter(user=user).first()
        if not checkCustomer:
            Customer.objects.create(user=user)
        checkCart = Cart.objects.filter(user=user)
        if not checkCart:
            Cart.objects.create(user=user)
        checkWishlist = Wishlist.objects.filter(user=user)
        if not checkWishlist:
            Wishlist.objects.create(user=user)
    # to render the homepage
    return render(request, "index.html")


@login_required
def cart(request):
    # to render the cart
    cart_id = Cart.objects.get_or_create(
        user=request.user, orderExecuted=False)

    cart_items = CartItem.objects.filter(cart=cart_id[0].id)
    return render(request, "cart.html", {"cart_items": cart_items})


@login_required
def wishlist(request):
    # to render the cart
    print(request.user)
    wishlist_id = Wishlist.objects.get(user=request.user)

    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist_id)
    return render(request, "wishlist.html", {"user": request.user, "wishlist_items": wishlist_items})


def products(request):

    # The products page has a form for sorting and filtering. If that form has been submitted, then the following code is executed

    if request.method == 'POST':

        print("+++++++READ FROM HERE++++++")

        # Getting all the submitted values from the form
        choice = request.POST.get('name')
        price = request.POST.get('price')
        gender = request.POST.get('gender')
        types = request.POST.get('types')
        use = request.POST.get('use')

        # Returning the form with the chosen values once the form has been submitted

        filter_form = FilterForm(initial={
                                 'name': choice, 'price': price, 'gender': gender, 'types': types, 'use': use})

        # Creating a QuerySet of all products in order to sort and filter them according to the choices

        unsorted_product = Product.objects.all()

        print("THE CHOICE IS")
        print(choice)
        print("THE PRICE IS")
        print(price)
        print("THE GENDER IS")
        print(gender)
        print("THE TYPE IS")
        print(types)
        print("THE USE IS")
        print(use)

        # Using lists to filter, explained in detail below
        genderList = []
        typesList = []
        useList = []

        # Initializing min and max price in order to set default values for filtering if no price filters are wanted

        min_price = 0.00
        max_price = 10000.00

        # Assigning values to max price on the basis of chosen price filter values. We assuming that the min price will
        # always be zero as if someone if willing to buy perfumes up to 5000 rupees, they will also be willing to buy
        # perfumes cheaper than that.

        if price == 'zero':
            max_price = 10000.00
        elif price == 'five':
            max_price = 500.00
        elif price == 'ten':
            max_price = 1000.00
        elif price == 'twenty':
            max_price = 2000.00
        elif price == 'thirty':
            max_price = 3000.00
        elif price == 'fourty':
            max_price = 4000.00
        elif price == 'fifty':
            max_price = 5000.00
        elif price == 'sixty':
            max_price = 6000.00
        elif price == 'seventy':
            max_price = 7000.00
        elif price == 'eighty':
            max_price = 8000.00

        print("MAX PRICE IS:", max_price)

        # In the following code, we accommodate for the case where the user does not want any filter of any particular kind.
        # In order to do this and also use one filter command, we use lists. In case the user chooses to have no filter, the list
        # will be populated by all possible values of that particular parameter. For instance, if no gender filter is chosen,
        # genderList will be populated by all genders - 'men' and 'women' and the filter will filter products that contain either
        # of them, effectively giving us all products with any gender property (all products). In case a value is chosen, the genderList
        # list will contain only that value and the filter command will filter products with only that gender.

        # Setting default genderlist value
        if gender == 'none':
            for pp in Tags.objects.all():
                genderList.append(pp)
        else:
            # Setting specific values and assigning to genderList
            if gender == 'men':
                gender_name = 'Men'
                genderList = [gender_name]
            if gender == 'women':
                gender_name = 'Women'
                genderList = [gender_name]

        print(genderList)

        # Repeating the same process for types and uses below

        if types == 'nothing':
            for pp in Product_Categories.objects.all():
                typesList.append(pp)
        else:
            if types == 'misc':
                types_name = 'misc'
                typesList = [types_name]
            if types == 'toilette':
                types_name = 'Eau De Toilette'
                typesList = [types_name]
            if types == 'parfum':
                types_name = 'Eau De Parfum'
                typesList = [types_name]

        print(typesList)

        if use == 'useless':
            for pp in subcategories.objects.all():
                useList.append(pp)
        else:
            if use == 'everyday':
                use_name = 'Everyday'
                useList = [use_name]
            if use == 'nightlife':
                use_name = 'Nightlife'
                useList = [use_name]
            if use == 'sporty':
                use_name = 'Sporty'
                useList = [use_name]

        print(useList)
        print("PRODUCTS BEFORE", unsorted_product)

        # Now to filter everything based on the choices and then put it into product. Using multiple filters and 'and' operators
        # in between in order to get a QuerySet with all filter conditions.

        unsorted_product = unsorted_product.filter(
            Q(price__gte=min_price),
            Q(price__lte=max_price),
            Q(tags__name__in=genderList),
            Q(category__name__in=typesList),
            Q(sub_categories__name__in=useList)
        )

        print(unsorted_product)

        # Once we have the filtered products, we can implement the sorting logic by using simple .order_by() commands.

        if choice == 'relevance':
            unsorted_product = unsorted_product.order_by('-inventory')

        if choice == 'popularity':
            unsorted_product = unsorted_product.order_by(
                '-popularity')

        if choice == 'low2high':
            unsorted_product = unsorted_product.order_by(
                'price')

        if choice == 'high2low':
            unsorted_product = unsorted_product.order_by(
                '-price')

        # Finally, to avoid duplicates in the final variable passed to the template, we put all products in a list
        # after checking if they already exist in the said list.

        product = []

        for val in unsorted_product:
            if val in product:
                continue
            else:
                product.append(val)

        # for item in product:
        #     print(item.price)

        return render(request, 'products.html', {"products": product, "filter_form": filter_form})

    # If the form has not been submitted and request method is GET, we execute the following code.
    else:

        # In order to link to the 'shop for men' and 'shop for women' section on the front page, we use the following code

        # This gets the parameters passed through the url as a search query
        params = request.GET
        print(params)

        # initializig initial QuerySet with all products
        unsorted_product = Product.objects.all()

        # checking if there is any parameter passed into the url.
        if params:
            # params is a dictionary with a key of gender and value of whatever is passed into the query
            print(params['gender'])

            # We use the same filtering system as above, using lists to filter and assigning values to the genderList
            # according to the value of params['gender'].

            if params['gender'] == 'men':
                gender_name = 'Men'
                genderList = [gender_name]
            elif params['gender'] == 'women':
                gender_name = 'Women'
                genderList = [gender_name]
            else:
                # To safeguard against manual changing of the url to make the value anything other than 'men' or 'women'
                genderList = []

            print("PRE", unsorted_product)

            # This makes sure that there is only a filter if genderList is populated, i.e. the correct query is passed in the url
            if len(genderList) > 0:
                unsorted_product = unsorted_product.filter(
                    Q(tags__name__in=genderList)
                )

            # Sorting the queryset on the basis of inventory to put the out of stock items at the bottom.
            unsorted_product = unsorted_product.order_by('-inventory')

            print("POST", unsorted_product)

            # To avoid duplicate products as done above
            product = []

            for val in unsorted_product:
                if val in product:
                    continue
                else:
                    product.append(val)

            # Setting filter form with all default values other than the gender value, which will be determined by what is chosen
            # on the home page ('Shop for Men' or 'Shop for Women')
            filter_form = FilterForm(
                initial={'name': 'relevance', 'price': 'zero', 'gender': params['gender'], 'types': 'nothing', 'use': 'useless'})

        # This case will be reached if the product page is reached without any filters or queries passed through urls
        else:
            # Setting all default filter and sort settings.
            filter_form = FilterForm(
                initial={'name': 'relevance', 'price': 'zero', 'gender': 'none', 'types': 'nothing', 'use': 'useless'})
            product = Product.objects.order_by('-inventory').all()

        return render(request, "products.html", {"products": product, "filter_form": filter_form})

    # sending to products.html file


def product(request, product_id):
    # specific product page, accessing data of each product through product ID primary key
    product = Product.objects.get(id=product_id)
    # getting average rating of product
    ratings = ReviewsRatings.objects.filter(product=product_id).all()
    avg = 0.0
    rcount = 0
    stars = [-1, -1, -1, -1, -1]
    for rating in ratings:
        avg += rating.rating
        rcount += 1
    if rcount == 0:
        avg = -1
    else:
        avg = avg / rcount
        avg = round(avg)
        for i in range(avg):
            stars[i] = 0

    # This would print out the stars in -1 and 0 format and it would be reflected in the visibility of the stars
    print(stars)

    # RECOMMENDATION ENGINE
    # Declaring an empty list and a count variable to check the number of recommendations
    recommended_list = []
    count = 0

    # First, we get all products with the same subcategory (which reflects the use case of the perfume: Everyday, Nightlife
    # and Sporty) and couple that with the same tag as the viewed product (which reflects gender). Putting the recommendations
    # in a list also removes the possibility of there being duplicates
    for sub in product.sub_categories.all():
        sub_id = subcategories.objects.get(id=sub.id)
        tag_id = Tags.objects.get(id=product.tags.first().id)
        sub_recco = Product.objects.filter(
            sub_categories=sub_id, tags=tag_id).exclude(id=product.id).exclude(inventory=0)[0:6]
        print(sub_recco)
        for rec in sub_recco:
            recommended_list.append(rec)
            count = count + 1

        print(count)
        print(recommended_list)

    # In case the above parameters do not give us 6 reccommendations, the engine then tries to get recommendations on
    # the basis of the category of the perfume (which referes to the type of the perfume: Eau de Toilette, Eau de Parfum and misc)
    # and does the same thing as above.
    if count < 6:
        for cat in product.category.all():
            cat_id = Product_Categories.objects.get(id=cat.id)
            tag_id = Tags.objects.get(id=product.tags.first().id)
            cat_recco = Product.objects.filter(
                category=cat_id, tags=tag_id).exclude(id=product.id).exclude(inventory=0)
            for item in recommended_list:
                cat_recco = cat_recco.exclude(name=item.name)
            print(cat_recco)
            for rec in cat_recco:
                recommended_list.append(rec)
                count = count + 1

            print(recommended_list)
            print(count)

    return render(request, "product_page.html", {"product": product, "rating": stars, "ratingsCount": rcount, "recommended": recommended_list[0:6], "user": request.user})


@login_required
def UpdateItem(request):
    # Using fetch, we send json data to the update item url. When the data reaches that url, this code parses that data
    # to give us the information we need. This information comes from cart.js
    data = json.loads(request.body)

    # Getting product ID and the action for that product
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    # Mapping that action and that product to a particular customer in order to add to their cart
    customer = request.user
    print(customer)
    product = Product.objects.get(id=productId)
    print(product)
    order = Cart.objects.get_or_create(
        user=customer, orderExecuted=False)[0]

    orderItem = CartItem.objects.get_or_create(
        cart=order, product=product)[0]
    print(orderItem)

    # Execution of action. Either adding or removing item from the cart
    if action == 'add':
        orderItem.quant = (orderItem.quant + 1)
        orderItem.save()

    elif action == 'remove':
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# The following wishlist code works the same way as the above update item code. The data comes from wishlist.js
@login_required
def UpdateWishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    print(customer)
    product = Product.objects.get(id=productId)
    print(product)
    wishlist = Wishlist.objects.get_or_create(
        user=customer, orderExecuted=False)[0]

    wishlistItem = WishlistItem.objects.get_or_create(
        wishlist=wishlist, product=product)[0]
    print(wishlistItem)

    if action == 'add':
        wishlistItem.save()
    elif action == 'remove':
        wishlistItem.delete()

    return JsonResponse('Item was added', safe=False)


# The following code gets all data about a user from the databse and passes it to the user page html template.
@login_required
def user(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    addresses = Addresses.objects.filter(customer=customer).all()
    print(addresses)
    orders = Cart.objects.filter(
        user=user, orderExecuted=True).all()
    orderHistory = []
    for order in orders:
        compOrder = completedOrders.objects.filter(order=order).all()
        for complete in compOrder:
            items = CartItem.objects.filter(cart=complete.order).all()
            print(items)
            orderHistory.append([complete, items])
    print(orderHistory)
    reviews = ReviewsRatings.objects.filter(user=user).all()
    print(reviews)
    checker = [-1, -1, -1, -1, -1]
    return render(request, "user.html", {"user": user, "addresses": addresses, "orderHistory": orderHistory, "reviews": reviews, "checker": checker})


@login_required
def order(request, cart_id):
    pass


def review(request, product_id):
    user = request.user
    ratings = ReviewsRatings.objects.filter(product=product_id).all()
    product = Product.objects.filter(id=product_id)[0]
    prod_id = product_id
    checker = [0, 0, 0, 0, 0]
    return render(request, "reviews.html", {"ratings": ratings, "checker": checker, "product_id": prod_id, "user": user, "product": product})


@login_required
def deleteReview(request, reviewsRatings_id):
    review = ReviewsRatings.objects.filter(id=reviewsRatings_id)
    print(review)
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.filter(id=product_id)
        review.delete()
        return redirect('review', product_id=product_id)


@login_required
def deleteWishlistItem(request, wishlistItem_id):
    wishlist_id = Wishlist.objects.filter(user=request.user)[0]
    if request.method == "POST":
        # Getting the user who is making the request
        product_id = request.POST.get("product_id")
        delete_wishlistitem = WishlistItem.objects.filter(
            wishlist=wishlist_id, product=product_id)
        delete_wishlistitem.delete()
        return redirect('wishlist')


@login_required
def deleteCartItem(request, cartItem_id):
    cartitem_id = Cart.objects.filter(user=request.user)[0]
    if request.method == "POST":
        print("hi")
        # Getting the user who is making the request
        product_id = request.POST.get("product_id")
        print("product_id")
        delete_cartitem = CartItem.objects.filter(
            cart=cartitem_id, product=product_id)
        print(delete_cartitem, "deletecart item")
        delete_cartitem.delete()
        return redirect('cart')


@login_required
def orderHistory(request):
    user = request.user
    orders = completedOrders.objects.filter(user=request.user).all()
    return render(request, "orderhistory.html")

    # prints the order history of the current customer


@login_required
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
        unsorted_product = main_product | product_categories | product_subcategories | product_tags

        product = []

        for val in unsorted_product:
            if val in product:
                continue
            else:
                product.append(val)

        # initializing the form and setting the default value to be relevance
        filter_form = FilterForm(
            initial={'name': 'relevance', 'price': 'zero', 'gender': 'none', 'types': 'nothing', 'use': 'useless'})
        return render(request, 'product_search.html', {"product": product, "search": search, "filter_form": filter_form})

    if request.method == 'POST':

        print("+++++++READ FROM HERE++++++")

        search = request.POST.get('searched')
        choice = request.POST.get('name')
        price = request.POST.get('price')
        gender = request.POST.get('gender')
        types = request.POST.get('types')
        use = request.POST.get('use')

        filter_form = FilterForm(initial={
                                 'name': choice, 'price': price, 'gender': gender, 'types': types, 'use': use})

        main_product = Product.objects.filter(name__icontains=search)
        product_categories = Product.objects.filter(
            category__name__icontains=search)
        product_subcategories = Product.objects.filter(
            sub_categories__name__icontains=search)
        product_tags = Product.objects.filter(
            tags__name__icontains=search)
        product = main_product | product_categories | product_subcategories | product_tags

        print("THE CHOICE IS")
        print(choice)
        print("THE PRICE IS")
        print(price)
        print("THE GENDER IS")
        print(gender)
        print("THE TYPE IS")
        print(types)
        print("THE USE IS")
        print(use)

        genderList = []
        typesList = []
        useList = []

        min_price = 0.00
        max_price = 10000.00

        if price == 'zero':
            max_price = 10000.00
        elif price == 'five':
            max_price = 500.00
        elif price == 'ten':
            max_price = 1000.00
        elif price == 'twenty':
            max_price = 2000.00
        elif price == 'thirty':
            max_price = 3000.00
        elif price == 'fourty':
            max_price = 4000.00
        elif price == 'fifty':
            max_price = 5000.00
        elif price == 'sixty':
            max_price = 6000.00
        elif price == 'seventy':
            max_price = 7000.00
        elif price == 'eighty':
            max_price = 8000.00

        print("MAX PRICE IS:", max_price)

        # print(priceList)

        if gender == 'none':
            for pp in Tags.objects.all():
                genderList.append(pp)
        else:
            if gender == 'men':
                gender_name = 'Men'
                genderList = [gender_name]
            if gender == 'women':
                gender_name = 'Women'
                genderList = [gender_name]

        print(genderList)

        if types == 'nothing':
            for pp in Product_Categories.objects.all():
                typesList.append(pp)
        else:
            if types == 'misc':
                types_name = 'misc'
                typesList = [types_name]
            if types == 'toilette':
                types_name = 'Eau De Toilette'
                typesList = [types_name]
            if types == 'parfum':
                types_name = 'Eau De Parfum'
                typesList = [types_name]

        print(typesList)

        if use == 'useless':
            for pp in subcategories.objects.all():
                useList.append(pp)
        else:
            if use == 'everyday':
                use_name = 'Everyday'
                useList = [use_name]
            if use == 'nightlife':
                use_name = 'Nightlife'
                useList = [use_name]
            if use == 'sporty':
                use_name = 'Sporty'
                useList = [use_name]

        print(useList)

        # Now to filter everything based on the choices and then put it into product

        product = product.filter(
            Q(price__gte=min_price),
            Q(price__lte=max_price),
            Q(tags__name__in=genderList),
            Q(category__name__in=typesList),
            Q(sub_categories__name__in=useList)
        )

        if choice == 'relevance':
            product = product

        if choice == 'popularity':
            product = product.order_by('-popularity')

        if choice == 'low2high':
            product = product.order_by('price')

        if choice == 'high2low':
            product = product.order_by('-price')

        return render(request, 'product_search.html', {"product": product, "search": search, "filter_form": filter_form})


def searchfilter(request):

    # if request.method == 'POST'

    pass
    # return render(request, 'product_search.html', {"product": product, "search": search, "form": form, "filter_form": filter_form})


def productfilter(request):
    pass
    # return render(request, 'product_search.html', {"product": product, "search": search, "form": form, "filter_form": filter_form})


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


@login_required
def newAddress(request):

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
        return redirect('user')


@login_required
def logoutuser(request):
    return render(request, "logoutuser.html")


@login_required
def orderConfirmed(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    current_cart = Cart.objects.get(user=user, orderExecuted=False)
    current_cart.orderExecuted = True
    current_cart.save()
    cart_items = CartItem.objects.filter(cart=current_cart.id)
    for product in cart_items:
        product.product.inventory = product.product.inventory-product.quant
        product.product.save()
    shippingaddress = request.POST.get('shippingaddress')
    paymentmethod = request.POST.get('paymentmethod')
    print(shippingaddress)
    print(paymentmethod)
    addy = Addresses.objects.filter(
        name=shippingaddress, customer=customer)[0]
    completedOrders.objects.create(order=current_cart, address=addy)
    return render(request, "orderconfirmed.html", {"user": user, "cart_items": cart_items, "shippingaddress": shippingaddress, "paymentmethod": paymentmethod, "current_cart": current_cart})
