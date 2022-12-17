from django.db import models
from django.contrib.auth import get_user_model
from store.models import Products,Variation

class Payment(models.Model):
    user=models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
    payment_id=models.CharField( max_length=100)
    payment_method=models.CharField( max_length=100)
    amount_paid=models.CharField( max_length=100)
    status=models.CharField( max_length=100)
    created_at=models.DateTimeField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS=(
        ("New" ,"New"),
        ("Accepted","Accepted"),
        ("Completed" , "Completed"),
        ("Cancelled" , "Cancelled")
    )
    user=models.ForeignKey(get_user_model(),  on_delete=models.SET_NULL ,null=True)
    payment=models.ForeignKey(Payment,  on_delete=models.SET_NULL , blank=True , null=True)
    order_number=models.CharField(max_length=200 , null=True , blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50 , blank=True)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    order_note=models.CharField(max_length=255 , blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=50 , choices=STATUS , default="New")
    ip=models.CharField(max_length=50 , blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField( auto_now=False, auto_now_add=True)
    updated_at=models.DateTimeField( auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    user=models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,  on_delete=models.SET_NULL ,blank=True , null=True)
    order=models.ForeignKey(Order,  on_delete=models.CASCADE)
    product=models.ForeignKey(Products,  on_delete=models.CASCADE)
    variation=models.ForeignKey(Variation,  on_delete=models.CASCADE)
    color=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    quantity=models.IntegerField()
    product_price=models.IntegerField()
    is_ordered=models.BooleanField()
    created_at=models.DateTimeField( auto_now=False, auto_now_add=True)
    updated_at=models.DateTimeField( auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.product.product_name





