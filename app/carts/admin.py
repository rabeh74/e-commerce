from django.contrib import admin
from carts.models import Cart ,CartItems

class CartItemAdmin(admin.ModelAdmin):
    list_display=['prducts' ,'cart','quauntity','is_active' ]



admin.site.register(Cart)
admin.site.register(CartItems , CartItemAdmin)
