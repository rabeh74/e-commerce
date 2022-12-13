from django.urls import path
from store.views import HomeView,ProductDetailView
from graphene_django.views import GraphQLView
from store.schema import schema

urlpatterns=[
    path('' , HomeView.as_view() , name='store'),
    path('category/<slug:slug>/' , HomeView.as_view() , name='products-by-category'),
    path('<slug:cat_slug>/<slug:slug>/' , ProductDetailView.as_view() , name='product-detail'),
    path('search/' , HomeView.as_view() , name='search'),
    path("graphql", GraphQLView.as_view(graphiql=True , schema=schema)),

]