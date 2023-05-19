import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


###################################################
#   Plantilla del panel de logueados, si no esta loqueado 
#   sera redirigido a la platilla der login
class PanelUsers(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    #Si el usuario no esta logueado lo redirigimos
    login_url = reverse_lazy(
        "user_app:loginUser"
    )


###################################################
class FechaMixin(object):
    class Meta:
        abstract = True
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context
    
    
###################################################
class TemplateMixin(FechaMixin ,TemplateView):
    template_name = "home/mixin.html"