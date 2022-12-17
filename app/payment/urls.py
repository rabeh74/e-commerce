from django.urls import path
from payment.views import PlaceOrderView
urlpatterns=[
    path("placeorder" ,PlaceOrderView.as_view() , name='placeorder' )
]