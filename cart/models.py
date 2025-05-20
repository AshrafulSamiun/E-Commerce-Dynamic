from django.db import models
from accounts.models import CustomUser
from products.models import TimeStampModel
from products.models import Product

# Create your models here.

class Cart(TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    session_key = models.CharField(max_length=255, blank=True, null=True)


class CartProduct(TimeStampModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products")
    quantity = models.PositiveIntegerField(default=0)
    

