from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# including paths for each feature

urlpatterns = [
    path('products/', views.products, name='products_view'),
    # unique path for each product depending on product id
    path('products/<int:product_id>/', views.product, name='product_page'),
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("search/", views.search, name="product_search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
