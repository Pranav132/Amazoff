from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products_view'),
    path('products/<int:product_id>/', views.product, name='product_page'),
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("search/", views.search, name="product_search"),
]
