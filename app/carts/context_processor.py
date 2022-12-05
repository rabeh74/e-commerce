from carts.views import _get_cart_id
from carts.models import Cart , CartItems

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}

    cart=Cart.objects.get(cart_id=_get_cart_id(request))
    cartitems=CartItems.objects.filter(cart=cart)

    for item in cartitems:
        cart_count +=item.quauntity

    return dict(cart_count=cart_count)
