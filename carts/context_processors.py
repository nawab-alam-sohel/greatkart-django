from .models import Cart, CartItem
from. views import _cart_id


from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0  # Initialize before using
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Get single Cart object
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)

