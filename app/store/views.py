from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,TemplateView,DetailView
from store.models import Products
from category.models import Category

class HomeView(ListView):
    template_name='store/store.html'
    context_object_name='prod'
    model=Products
    queryset=Products.objects.all()

    def get_queryset(self):
        sulg=self.kwargs.get('slug' , None)
        if sulg:
            cat=Category.objects.get(slug=self.kwargs["slug"])
            return self.queryset.filter(is_available=True , category=cat)
        return self.queryset.filter(is_available=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_nums"] = self.get_queryset().count()
        return context

class ProductDetailView(DetailView):
    template_name='store/product.html'
    context_object_name='product'
    model=Products

    def get_object(self , queryset=None):
        cat=self.kwargs.get('cat_slug')
        slug=self.kwargs.get(self.slug_url_kwarg)

        return self.model.objects.filter(category__slug=cat,slug=slug)[0]





