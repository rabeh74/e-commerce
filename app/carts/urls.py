from django.urls import path
from carts.views import (CartView,
    add_to_cart,
    delete_from_cart,
    delete_cart_item,
    CheckOutView

    )
urlpatterns=[
    path('' ,CartView.as_view() , name='cart'),
    path('add/<int:pk>/' ,add_to_cart , name='add-cart' ),
    path('remove/<int:pk>/<int:cart_pk>/' ,delete_from_cart , name='remove-cart' ),
    path('remove-cart-item /<int:pk>/<int:cart_pk>/' ,delete_cart_item , name='remove-cart-item'),
    path('checkout' , CheckOutView.as_view() , name='checkout')
]