from django.forms import ModelForm
from payment.models import Order
class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=("first_name" , "last_name" , "phone_number" , "email" , "address_line1",\
            "address_line2" , "country" , "state" , "city" ,"order_note")