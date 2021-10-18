from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def product(request):
    return HttpResponse("<h1>Hello, these are our products</h1>")
