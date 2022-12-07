from django.forms import ModelForm
from store.models import Variation

class AddForm(ModelForm):
    class Meta:
        model=Variation
        fields="__all__"
