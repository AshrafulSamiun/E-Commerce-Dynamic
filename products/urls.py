from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("all_products", views.all_products, name="all_products"),
    path("product_wishlist/<slug:product_slug>/", views.product_wishlist, name="product_wishlist"),
    path(
        "categories/<slug:category_slug>/products",
        views.category_products,
        name="category_products",
    ),
    path("products/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path(
        "products/<slug:product_slug>/review/",
        views.submit_review,
        name="submit_review",
    ),
   # path('remove_cart/<slug:product_slug>/', views.remove_cart, name='remove_cart'),
]
