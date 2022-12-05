from django.shortcuts import render
from carts.models import Cart,CartItems
from store.models import Products
from django.views.generic import TemplateView,RedirectView

def _get_cart_id(request):
        cart_id=request.session.session_key
        if not cart_id:
            cart=request.session.create()
        return cart_id

class CartView(TemplateView):
    
    template_name='store/cart.html'

    def get_context_data(self, **kwargs):
        quantity=0
        total=0
        context = super().get_context_data(**kwargs)
        try:
            cart_id=_get_cart_id(self.request)
            cart=Cart.objects.get(cart_id=cart_id)
            cartitems=CartItems.objects.filter(cart=cart , is_active=True)

            for cartitem in cartitems:
                total += (cartitem.prducts.price * cartitem.quauntity)
                quantity += cartitem.quauntity
            tax=(2*total)/100
            grand_total=tax +total
            context['total']=total
            context['quantity']=quantity
            context['cart_items']=cartitems
            context['tax']=tax
            context['grand_total']=grand_total
        except:
            pass

        return context


class AddCartView(RedirectView):
    pattern_name= 'cart'

    def _get_cart_id(self):
        cart_id=self.request.session.session_key
        if not cart_id:
            cart=self.request.session.create()
        return cart_id

    def get_redirect_url(self, *args, **kwargs):
        ''' map cart id to session key in cookies '''
        pk=kwargs['pk']
        kwargs.pop('pk')
        product=Products.objects.get(pk=pk)
        try:
            cart=Cart.objects.get(cart_id=self._get_cart_id())
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=self._get_cart_id())
        cart.save()

        try:
            cart_item=CartItems.objects.get(cart=cart , prducts=product)
            cart_item.quauntity +=1
        except  CartItems.DoesNotExist:
            cart_item=CartItems.objects.create(
                    cart=cart,
                    prducts=product,
                    quauntity=1
                )

        cart_item.save()
        return super().get_redirect_url(*args, **kwargs)
class DeleteFromCart(RedirectView):
    pattern_name='cart'

    def _get_cart_id(self):
        cart_id=self.request.session.session_key
        if not cart_id:
            cart=self.request.session.create()
        return cart_id

    def get_redirect_url(self,*args, **kwargs):
        cart=Cart.objects.get(cart_id=self._get_cart_id())

        pk=kwargs.get('pk' , None)
        kwargs.pop('pk')

        product=Products.objects.get(pk=pk)
        try:
            cart=Cart.objects.get(cart_id=self._get_cart_id())
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=self._get_cart_id())
        cart.save()

        cartitem=CartItems.objects.get(cart=cart , prducts=product)
        if cartitem.quauntity >1:
            cartitem.quauntity -=1
            cartitem.save()
        else:
            cartitem.delete()

        return super().get_redirect_url(*args, **kwargs)

class RemoveCartItem(RedirectView):
    pattern_name='cart'

    def _get_cart_id(self):
        cart_id=self.request.session.session_key
        if not cart_id:
            cart=self.request.session.create()
        return cart_id

    def get_redirect_url(self,*args, **kwargs):
        cart=Cart.objects.get(cart_id=self._get_cart_id())

        pk=kwargs['pk']
        kwargs.pop('pk')

        product=Products.objects.get(pk=pk)

        cart=Cart.objects.get(cart_id=self._get_cart_id())

        cartitem=CartItems.objects.get(cart=cart , prducts=product)
        cartitem.delete()
        return super().get_redirect_url(*args, **kwargs)
