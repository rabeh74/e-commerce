from django.urls import path
from store.views import HomeView,ProductDetailView

urlpatterns=[
    path('' , HomeView.as_view() , name='store'),
    path('<slug:slug>/' , HomeView.as_view() , name='products-by-category'),
    path('<slug:cat_slug>/<slug:slug>/' , ProductDetailView.as_view() , name='product-detail'),

]