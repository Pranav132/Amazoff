from django.http import HttpResponse
from products.models import Product
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, "index.html")


def products(request):
    products = Product.objects.all()
    prods = []
    for product in products:
        prods.append([product.id, product.name, product.site_title, product.price,
                      product.description, product.tags, product.popularity])

    return render(request, "products.html", {"products": products})


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product_page.html", {"product": product})


def search(request):
    if request.method == 'POST':
        search = request.POST['searched']
        product = Product.objects.filter(name__icontains=search)
        return render(request, 'product_search.html', {"product": product, "search": search})
        # return HttpResponse("<h1>Search works only.</h1>")
