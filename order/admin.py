from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.
admin.site.register([
    Order,
    OrderProduct,
    Payment
])