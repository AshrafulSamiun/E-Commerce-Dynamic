from products.models import Category
from cart.models import Cart, CartProduct
from cart.utils import get_session_key  # adjust import if needed
from django.conf import settings

def global_context(request):
    categories = Category.objects.all()
    cart_total_quantity = 0
    cart_total_amount = 0

    cart = None

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = get_session_key(request)
        cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        cart_items = CartProduct.objects.filter(cart=cart).select_related("product")
        cart_total_quantity = sum(item.quantity for item in cart_items)
        cart_total_amount = sum(item.quantity * item.product.price for item in cart_items)

    return {
        'menu_categories': categories,
        'cart_total_quantity': cart_total_quantity,
        'cart_total_amount': cart_total_amount,
         "MEDIA_URL": settings.MEDIA_URL,
    }
