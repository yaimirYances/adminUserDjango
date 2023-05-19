from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.

from .managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    
    GENERO= (
        ("M","Masculino"),
        ("M","Femenino"),
    )
    
    username = models.CharField(max_length=50,  unique=True)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField(default=False)
    nombres = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO, blank=True)
    codregistro = models.CharField(max_length= 6, blank=True)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    objects = UserManager()
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + " " + self.apellidos