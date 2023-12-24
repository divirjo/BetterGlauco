from django.urls import path
from .views import InicioOperacao


app_name='invest_operacao'

urlpatterns = [
    path('', 
         InicioOperacao.as_view(), 
         name='inicio_operacao'),
     
    ]