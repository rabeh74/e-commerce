from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from payment.forms import OrderForm
from carts.models import CartItems
from django.views.generic import CreateView
import datetime
from django.http import HttpResponseRedirect,HttpResponse

class PlaceOrderView(CreateView):
    template_name='store/checkout.html'
    success_url=reverse_lazy('dashboard')
    form_class=OrderForm
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def calculate_other_fields(self):
        user=self.request.user
        total=0
        quantity=0
        cart_items=CartItems.objects.filter(user=user)
        for cartitem in cart_items:
                total += (cartitem.prducts.price * cartitem.quauntity)
                quantity += cartitem.quauntity
        tax=(2*total)/100
        grand_total=tax +total
        print(grand_total , tax)
        return tax , grand_total
    def form_valid(self, form):
        self.object=form.save(commit=False)


        self.object.user=self.request.user
        tax,grand_total=self.calculate_other_fields()
        self.object.tax=tax
        self.object.order_total=grand_total
        self.object.ip=self.request.META.get("REMOTE_ADDR")

        yr=int(datetime.date.today().strftime("%Y"))
        mt=int(datetime.date.today().strftime("%m"))
        dy=int(datetime.date.today().strftime("%d"))
        d=datetime.date(yr ,mt , dy)
        current_date=d.strftime("%Y%m%d")
        self.object.order_number = current_date+str(self.object.id)
        
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        quantity=0
        total=0
        context = super().get_context_data(**kwargs)
        try:

            if self.request.user.is_authenticated:
                cartitems=CartItems.objects.filter(user=self.request.user)
            else:
                cart_id=_get_cart_id(self.request)
                cart=Cart.objects.get(cart_id=cart_id)
                cartitems=CartItems.objects.filter(cart=cart)

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
