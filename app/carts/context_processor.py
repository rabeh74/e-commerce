from carts.views import _get_cart_id
from carts.models import Cart , CartItems

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    try:
        if request.user.is_authenticated:
            cartitems=CartItems.objects.filter(user=request.user)
        else:
            cart=Cart.objects.filter(cart_id=_get_cart_id(request))
            cartitems=CartItems.objects.filter(cart=cart[:1])

        for item in cartitems:
            cart_count +=item.quauntity
    except:
        cart_count=0

    return dict(cart_count=cart_count)
