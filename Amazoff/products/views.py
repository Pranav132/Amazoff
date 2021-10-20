from django.http import HttpResponse
from products.models import Product
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, "index.html")


def product(request):
    products = Product.objects.all().filter(inventory=1)
    for product in products:
        print(product.tags)
    return HttpResponse("<h1>Hello, these are our products</h1>")

def search(request):
    if request.method == 'POST':
        search= request.POST['searched']
        product = Product.objects.filter(name__icontains=search)
        return render (request, 'product_search.html', {"product":product, "search":search})
        # return HttpResponse("<h1>Search works only.</h1>")