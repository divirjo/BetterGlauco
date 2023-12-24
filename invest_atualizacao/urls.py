from django.urls import path
from .views import InicioAtualizacao



app_name='invest_atualizacao'

urlpatterns = [
    path('', 
         InicioAtualizacao.as_view(), 
         name='inicio_atualizacao'),
     
    ]