from django.db import models
from uuid import uuid4
from store.models import Products
from store.models import Variation

class Cart(models.Model):

    cart_id=models.CharField( max_length=255 , blank=True , unique=True)
    date_added=models.DateField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItems(models.Model):
    variation=models.ManyToManyField(Variation, blank=True)
    prducts=models.ForeignKey(Products, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quauntity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.prducts.price * self.quauntity



    def __str__(self):
        return self.prducts.product_name
    class Meta:
        ordering=("-id",)




