from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationCodeForm
from .models import User
from .funtions import code_generator


#############################################################
class UserRegister(FormView):
    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = '/'
    
    class Meta:

        verbose_name = 'UserRegister'
        verbose_name_plural = 'UserRegisters'

    def form_valid(self, form):
        #Generando codigo de verificacion
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password1"],
            #Extra_fields
            nombres = form.cleaned_data["nombres"],
            apellidos = form.cleaned_data["apellidos"],
            genero = form.cleaned_data["genero"],
            codregistro = codigo,
        )
        #Enviar el codigo al email del usuario
        asunto = "Confimacion de email de registro"
        mensaje = "Codigo de registro: "+codigo
        remitente = "jamaicabarbershop1@gmail.com"
        send_mail(asunto, mensaje, remitente, [form.cleaned_data["email"],])
            #redirigir a plantilla de validacion
        return HttpResponseRedirect(
            reverse(
                "user_app:verificationUser",
                kwargs={"pk":usuario.id}
            )
        )
    
    
#############################################################
class CodeVericationView(FormView):
    template_name = "user/verification.html"
    form_class = VerificationCodeForm
    success_url = reverse_lazy(
        "user_app:loginUser"
    )
    
    class Meta:
        verbose_name = 'Verificacion'
        verbose_name_plural = 'Verificaciones'
        
    #Enviando informacion al formulario para poder recuperar datos por url
    #en el formulario
    def get_form_kwargs(self):
        #sobrescribiendo
        kwargs = super(CodeVericationView, self).get_form_kwargs()
        kwargs.update({
            "pk":self.kwargs["pk"]
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs["pk"]
        ).update(
            is_active = True
        )
        return super().form_valid(form)

#############################################################
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
    
    
#############################################################
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
        
        
#############################################################
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "user/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy(
        "user_app:loginUser"
    )
    login_url = reverse_lazy(
        "user_app:loginUser"
    )
    
    class Meta:
        verbose_name = 'UpdatePasswordView'
        verbose_name_plural = 'UpdatePasswordViews'

    def form_valid(self, form):
        #Verificar si el usuario esta activo
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data["password1"]
        )
        #validamos si la autenticacion es correcta
        if user:
            new_password = form.cleaned_data["password2"]
            usuario.set_password(new_password)
            usuario.save()
            
        logout(self.request)
        return super().form_valid(form)
    
    #CLAVE: ikcaqjavskmympoa