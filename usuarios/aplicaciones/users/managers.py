from django.db import models
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager, models.Manager):
    
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        #Encryptando password
        user.set_password(password)
        #Expecificando la base de datoss donde se va aguardar
        user.save(using=self.db)
        return user
    
    
    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)