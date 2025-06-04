from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartProduct
from products.models import Product

from .utils import get_session_key

def add_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    try :
        cart = Cart.objects.get(session_key=get_session_key(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=get_session_key(request), user=request.user if request.user.is_authenticated else None)


    try:
        cart_product = CartProduct.objects.get(cart=cart, product=product)
    
    except CartProduct.DoesNotExist:
        cart_product = CartProduct.objects.create(cart=cart, product=product,quantity=0)

    cart_product.quantity += 1
    cart_product.save()
    messages.success(request, f"{product.name} has been added to your cart.")
    
    url= request.META.get("HTTP_REFERER")
    return redirect(url)


def remove_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart = get_object_or_404(Cart, session_key=get_session_key(request))
   
    cart_product =get_object_or_404(CartProduct, cart=cart, product=product)
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    else:   
        cart_product.delete()
    
    url= request.META.get("HTTP_REFERER")
    return redirect(url)


def cart_detail(request, total=0, quantity=0, cart_items=None):    

    if request.user.is_authenticated:
        #return HttpResponse("This is a placeholder for the cart detail view. Implement your logic here.")
        #cart = get_object_or_404(Cart, user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        #cart = get_object_or_404(Cart, session_key=get_session_key(request))
        #return HttpResponse(get_session_key(request))
        cart, created = Cart.objects.get_or_create( session_key=get_session_key(request))


    cart_items = CartProduct.objects.filter(cart=cart).select_related("product")
    total = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "discount":0,
        "delivery_charge": settings.DELIVERY_CHARGE,
        "grand_total": total + settings.DELIVERY_CHARGE,
    }
    return render(request, "carts/cart.html", context)