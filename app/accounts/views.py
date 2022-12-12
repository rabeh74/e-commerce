from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from accounts.forms import RegisterationFrom,Loginform
from django.contrib.auth import get_user_model,logout
from django.views.generic import CreateView,TemplateView,FormView,RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class RegestraionView(SuccessMessageMixin,FormView):
    template_name='accounts/register.html'
    form_class=RegisterationFrom
    success_message='you are welcome '

    def form_valid(self, form):
        user_name=form.cleaned_data['email'].split('@')[0]
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        password=form.cleaned_data['password']
        email=form.cleaned_data['email']
        phone_number=form.cleaned_data['phone_number']

        user=get_user_model().objects.create_user(
            email=email,
            first_name=first_name, user_name=user_name,
            last_name=last_name,
            password=password,
        )
        user.phone_number=phone_number
        user.save()
        cur_site=get_current_site(self.request)
        mail_subject= " Please activate you account "
        to_email=email
        message=render_to_string("accounts/veridication.html" , {
            'user':user,
            'domain':cur_site,
            'token':default_token_generator.make_token(user),
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        })
        send_message=EmailMessage(mail_subject , message ,to=[to_email])
        send_message.send()


        return redirect('login/?command=verification&email='+email)

class Login(LoginView):
    template_name='accounts/login.html'
    authentication_form=Loginform
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, "bad credionatls.")
        return super().form_invalid(form)
    def form_valid(self, form):
        messages.success(self.request , " You are now logged in ")
        return super().form_valid(form)


class Logout(LoginRequiredMixin,RedirectView):
    login_url = reverse_lazy('login')
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        messages.add_message(self.request, messages.SUCCESS, "logout done correctly")
        return super().get_redirect_url(*args, **kwargs)

class DashBoard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('home')
    template_name='accounts/dashboard.html'

def activate(request , uidb64 , token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user=get_user_model()._default_manager.get(pk=uid)

    except(ValueError , TypeError , get_user_model().DoesNotExist , OverflowError):
        user=None

    if user and default_token_generator.check_token(user , token):
        user.is_active=True
        user.save()
        messages.success(request, 'congratulation conformation of registartion is done')

        return redirect('login')

    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')
def ForgetPassword(request):
    if request.method=="POST":
        email=request.POST['email']
        if get_user_model().objects.filter(email__exact=email):
            user=get_user_model().objects.get(email=email)

            cur_site=get_current_site(request)
            mail_subject= " Reset password "
            to_email=email
            message=render_to_string("accounts/ResetPass.html" , {
                'user':user,
                'domain':cur_site,
                'token':default_token_generator.make_token(user),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            })
            send_message=EmailMessage(mail_subject , message ,to=[to_email])
            send_message.send()
            messages.success(request, "password Reset email has been sent to your email ")
            return redirect('login')

        else:
            messages.warning(request, 'your email does not exist')
            return redirect('forgetpassword')
    else:
        return render(request, "accounts/forgot_password.html")


def resetpassword_validate(request , uidb64 , token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=get_user_model().objects.get(pk=uid)
    except (ValueError, get_user_model().DoesNotExist,TypeError , OverflowError):
        user=None

    if user and default_token_generator.check_token(user , token):
        request.session['uid']=uid
        messages.success(request, 'please reset password ')
        return redirect('resetpassword')
    else:
        messages.error(request, 'invalid Reset link')
        return redirect('forgetpassword')
def resetpassword(request):
    if request.method=="POST":
        pk=request.session['uid']
        user=get_user_model().objects.get(pk=pk)
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 ==pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request, 'reset password done correctly')
            return redirect('login')
        else:
            messages.warning(request, 'two password does not match')
            return redirect('resetpassword')
    return render(request, "accounts/resetpassword.html")


