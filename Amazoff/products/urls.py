from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product, name='product_view'),
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("search/", views.search, name="product_search"),
]
