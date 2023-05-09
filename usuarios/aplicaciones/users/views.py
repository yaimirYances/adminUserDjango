from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.views.generic import View
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import UserRegisterForm, LoginForm
from .models import User

class UserRegister(FormView):
    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = '/'
    
    class Meta:

        verbose_name = 'UserRegister'
        verbose_name_plural = 'UserRegisters'

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password1"],
            #Extra_fields
            nombres = form.cleaned_data["nombres"],
            apellidos = form.cleaned_data["apellidos"],
            genero = form.cleaned_data["genero"],
        )
        return super().form_valid(form)
    

#########################################
class LoginUser(FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    success_url = reverse_lazy(
        "home_app:panel"
    )
    
    class Meta:
        verbose_name = 'LoginUser'
        verbose_name_plural = 'LoginUsers'

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data["username"],
            password = form.cleaned_data["password"]
        )
        login(self.request, user)
        return super().form_valid(form)
    
    
#########################################
class LogoutUser(View):    
    class Meta:
        verbose_name = 'LoginUser'
        verbose_name_plural = 'LoginUsers'

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                "user_app:loginUser"
            )
        )