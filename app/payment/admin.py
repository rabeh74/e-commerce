from django.contrib import admin
from payment.models import Payment , Order , OrderProduct

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
