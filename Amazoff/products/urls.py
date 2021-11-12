from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# including paths for each feature

urlpatterns = [
    path('products/', views.products, name='products'),
    # unique path for each product depending on product id
    path('products/<int:product_id>/', views.product, name='product_page'),
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("cart/", views.cart, name="cart"),
    path("search/", views.search, name="product_search"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
