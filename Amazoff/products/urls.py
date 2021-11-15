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
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("cart/", views.cart, name="cart"),
    path("search/", views.search, name="product_search"),
    path("update_item/", views.UpdateItem, name='update_item'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path("user/", views.user, name="user"),
    path("order/<int:cart_id>", views.order, name="order"),
    path("review/<int:product_id>", views.review, name="review"),
    path("newReview/<int:product_id>", views.newReview, name="newReview"),
    path("orderHistory", views.orderHistory, name="orderHistory"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
