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
    path("cart/", views.cart, name="cart"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("checkout/", views.checkout, name="checkout"),
    path("search/", views.search, name="product_search"),
    path("update_item/", views.UpdateItem, name='update_item'),
    path("update_wishlist/", views.UpdateWishlist, name='update_wishlist'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
    path("user/", views.user, name="user"),
    path("order/<int:cart_id>", views.order, name="order"),
    path("review/<int:product_id>", views.review, name="review"),
    path("newAddress/", views.newAddress, name="newAddress"),
    path("orderconfirmed/", views.orderConfirmed, name="orderconfirmed"),
    path("newReview/<int:product_id>", views.newReview, name="newReview"),
    path("orderHistory", views.orderHistory, name="orderHistory"),
    path("deleteReview/<int:reviewsRatings_id>",
         views.deleteReview, name="deleteReview"),
    path("deleteWishlistItem/<int:wishlistItem_id>",
         views.deleteWishlistItem, name="deleteWishlistItem"),
    path("deleteCartItem/<int:cartItem_id>",
         views.deleteCartItem, name="deleteCartItem"),
    path("logoutuser/", views.logoutuser, name="logoutuser"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
