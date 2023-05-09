from django.urls import path
from . import views

app_name = "home_app"

urlpatterns = [
    path('panel/', views.PanelUsers.as_view(), name="panel"),
    path('mixin/', views.TemplateMixin.as_view(), name="mixin"),
]