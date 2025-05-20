from django.urls import path, include
from . import views

urlpatterns = [
    path("add_cart/<slug:product_slug>/", views.add_cart, name="add_cart"),
    path("remove_cart/<slug:product_slug>/", views.remove_cart, name="remove_cart"),
    path("", views.cart_detail, name="cart"),
    # path("checkout/", views.checkout, name="checkout"),
]