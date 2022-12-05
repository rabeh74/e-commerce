from django.urls import path
from carts.views import (CartView,
    AddCartView,DeleteFromCart,
    RemoveCartItem

    )
urlpatterns=[
    path('' ,CartView.as_view() , name='cart'),
    path('add/<int:pk>/' ,AddCartView.as_view() , name='add-cart' ),
    path('remove/<int:pk>/' ,DeleteFromCart.as_view() , name='remove-cart' ),
    path('remove-cart-item <int:pk>/' ,RemoveCartItem.as_view() , name='remove-cart-item')
]