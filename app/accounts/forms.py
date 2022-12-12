from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
class RegisterationFrom(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={
        'placeholder':'enter password'
    }
    ))
    confirm_pass=forms.CharField(widget=forms.PasswordInput(
        attrs={
        'placeholder':'confirm password'
    }
    ))
    class Meta:
        model=get_user_model()
        fields=['first_name' , 'last_name' ,'phone_number' , 'email' , 'password' , 'confirm_pass']

    def __init__(self,*args , **kwargs):
        super(RegisterationFrom, self).__init__(*args , **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']='enter your first name'
        self.fields['last_name'].widget.attrs['placeholder']='enter your last name'
        self.fields['phone_number'].widget.attrs['placeholder']='enter your phone'
        self.fields['email'].widget.attrs['placeholder']='enter your email'

        for field_key , field_val in self.fields.items():
            field_val.widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data['password']
        confirm_passworf=cleaned_data['confirm_pass']

        if password != confirm_passworf:
            raise forms.ValidationError('passwords does not math ')

        return cleaned_data
class Loginform(AuthenticationForm):
    def __init__(self,*args , **kwargs):
        super().__init__(*args , **kwargs)

        self.fields['password'].widget.attrs['placeholder']='enter your password'
        self.fields['username'].widget.attrs['placeholder']='enter your email'

        for field_key , field_val in self.fields.items():
            field_val.widget.attrs['class']='form-control'

