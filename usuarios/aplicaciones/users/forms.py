from django import forms
from django.contrib.auth import authenticate
from .models import User


##############################################################
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña"
            }
        )
    )
    
    password2 = forms.CharField(
        label = "Confirmar contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "placeholder": "Repetir contraseña"
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "nombres",
            "apellidos",
            "genero",
        )

    #validando la clave  de acceso

    def clean_password2(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error("password2", "Las contraseñas mo son iguales")
            
            
##############################################################          
class LoginForm(forms.Form):
    username = forms.CharField(
        label = "username",
        required = True,
        widget = forms.TextInput(
            attrs={
                "placeholder": "username",
                "style": "{margin:10px}",
            }
        )
    )
    
    password = forms.CharField(
        label = "contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "style": "{margin:10px}",
            }
        )
    )

    #Validadndo valores ingresados al login, si existen
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        
        if not authenticate(username = username, password = password):
            raise forms.ValidationError(
                "Los datos no son correctos"
            )
        return self.cleaned_data

    
##############################################################          
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label = "contraseña actual",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña actual",
                "style": "{margin:10px}",
            }
        )
    )
    
    password2 = forms.CharField(
        label = "contraseña nueva",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña nueva",
                "style": "{margin:10px}",
            }
        )
    )
    
    
##############################################################          
class VerificationCodeForm(forms.Form):
    codregistro = forms.CharField(
        label = "Codigo de verificacion",
        required = True,
        widget = forms.TextInput(
            attrs={
                "placeholder": "codigo de verificacion",
                "style": "{margin:10px}",
            }
        )
    )
    
    #inicializando datos
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationCodeForm, self).__init__(*args, **kwargs)
    
    #Validando campo en especifico
    def clean_codregistro(self):
        codigo = self.cleaned_data["codregistro"]
        if len(codigo) == 6:
            #Verificamos si el codigo y el id son validos
            activo = User.objects.cod_validacion(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError("Codigo no es correcto")
        else:
            raise forms.ValidationError("Codigo no es correcto")