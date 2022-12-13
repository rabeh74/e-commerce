from django.shortcuts import render
from carts.models import Cart,CartItems,Variation
from store.models import Products
from django.views.generic import TemplateView,RedirectView,FormView
from django.http import HttpResponse
from store.forms import AddForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(TemplateView):

    template_name='store/cart.html'

    def get_context_data(self, **kwargs):
        quantity=0
        total=0
        context = super().get_context_data(**kwargs)
        try:
            cart_id=_get_cart_id(self.request)
            if self.request.user.is_authenticated:
                cartitems=CartItems.objects.filter(user=self.request.user , is_active=True)
            else:
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
def _get_cart_id(request):
        cart_id=request.session.session_key
        if not cart_id:
            cart_id=request.session.create()
            print(cart_id)
        print(cart_id)
        return cart_id

def add_to_cart(request , pk , item_id=None):
    color=request.POST.get('color' ,None)
    size=request.POST.get('size' , None)
    product=get_object_or_404(Products , pk=pk)

    var=[]
    if color:
        var.append(Variation.objects.get(product=product, variation_category__iexact='color' , variation_value__iexact=color))
    if size:
        var.append(Variation.objects.get(product=product,variation_category__iexact='size' , variation_value__iexact=size))
    if request.user.is_authenticated:
        is_cart_item_exist=CartItems.objects.filter(user=request.user , prducts=product).exists()
        if is_cart_item_exist:
            cart_item=CartItems.objects.filter(user=request.user , prducts=product)
            id=None
            flag=False
            if len(var)>0:
                for item in cart_item:
                    if var == list(item.variation.all()):
                        id=item.id
                        flag=True
                        break
            if flag :
                cart_item=cart_item.get(id=id)
                cart_item.quauntity +=1

            else:
                cart_item=CartItems.objects.create(
                quauntity=1,
                prducts=product,
                user=request.user)

                for v in var:
                    cart_item.variation.add(v)

            cart_item.save()



        else:
            cart_item=CartItems.objects.create(
                quauntity=1,
                prducts=product,
                user=request.user
            )
            for v in var:
                cart_item.variation.add(v)
            cart_item.save()


        return redirect('cart')
    else:


        try:
            cart=Cart.objects.get(cart_id=_get_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_get_cart_id(request))
        cart.save()
        is_cart_item_exist=CartItems.objects.filter(cart=cart , prducts=product).exists()
        if is_cart_item_exist:
            cart_item=CartItems.objects.filter(cart=cart , prducts=product)
            id=None
            flag=False
            if len(var)>0:
                for item in cart_item:
                    if var == list(item.variation.all()):
                        id=item.id
                        flag=True
                        break
            if flag :
                cart_item=cart_item.get(id=id)
                cart_item.quauntity +=1

            else:
                cart_item=CartItems.objects.create(
                quauntity=1,
                prducts=product,
                cart=cart)

                for v in var:
                    cart_item.variation.add(v)

            cart_item.save()



        else:
            cart_item=CartItems.objects.create(
                quauntity=1,
                prducts=product,
                cart=cart
            )
            for v in var:
                cart_item.variation.add(v)
            cart_item.save()


        return redirect('cart')

def delete_from_cart(request , pk ,cart_pk):
    prducts=Products.objects.get(pk=pk)


    if request.user.is_authenticated:
        print(" hello " , request.user , prducts , cart_pk)
        cart_item=CartItems.objects.get(user=request.user , prducts=prducts , id=cart_pk )
    else:
        cart=Cart.objects.get(cart_id= _get_cart_id(request))
        cart_item=CartItems.objects.get( cart=cart , prducts=prducts , id=cart_pk )


    try:

        if cart_item.quauntity <=1:
            cart_item.delete()
        else:
            cart_item.quauntity -=1
            cart_item.save()
    except:
        pass
    return redirect('cart')

def delete_cart_item(request ,pk , cart_pk):
    products=Products.objects.get(pk=pk)

    if request.user.is_authenticated:
        cart_item=CartItems.objects.get(user=request.user , prducts=products , id=cart_pk )
    else:
        cart=Cart.objects.get(cart_id= _get_cart_id(request))
        cart_item=CartItems.objects.get(pk=cart_pk , cart=cart , prducts=products)
    cart_item.delete()

    return redirect('cart')

class CheckOutView(LoginRequiredMixin,TemplateView):
    template_name='store/checkout.html'

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