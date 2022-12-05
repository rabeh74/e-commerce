from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,TemplateView,DetailView
from store.models import Products
from category.models import Category
from carts.models import CartItems
from django.db.models import Q

class HomeView(ListView):
    template_name='store/store.html'
    context_object_name='prod'
    model=Products
    queryset=Products.objects.all()
    paginate_by=4

    def get_queryset(self):
        sulg=self.kwargs.get('slug' , None)
        if sulg:
            cat=Category.objects.get(slug=self.kwargs["slug"])
            return self.queryset.filter(is_available=True , category=cat).order_by('-id')
        search=self.request.GET.get('search' , None)
        if search:
            return self.queryset.filter(\
                 Q(product_name__icontains=search) | Q(description__icontains=search)).order_by('-id')
        return self.queryset.filter(is_available=True).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_nums"] = self.get_queryset().count()
        return context

class ProductDetailView(DetailView):
    template_name='store/product.html'
    context_object_name='product'
    model=Products

    def _get_cart_id(self):
        cart_id=self.request.session.session_key
        if not cart_id:
            cart=self.request.session.create()
        return cart_id
    def get_object(self , queryset=None):
        cat=self.kwargs.get('cat_slug')
        slug=self.kwargs.get(self.slug_url_kwarg)

        return self.model.objects.filter(category__slug=cat,slug=slug)[0]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product=self.get_object()
        in_cart=CartItems.objects.filter(cart__cart_id=self._get_cart_id() , prducts=product).exists()
        context['in_cart']=in_cart


        return context




