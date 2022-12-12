from django.views.generic import ListView
from store.models import Products

class HomeView(ListView ):

    model =Products
    context_object_name='products'
    template_name='home.html'
    queryset=Products.objects.all()

    def get_queryset(self):

        return self.queryset.filter(is_available=True)[:4]
