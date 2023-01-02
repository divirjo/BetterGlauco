from django.urls import path
from .views import Ajuda, HomeInvestimento, Valor_compra


app_name='investimento'

urlpatterns = [
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    path('help/', Ajuda.as_view(), name='ajuda_inicio'),
    path('valor_compra/', Valor_compra.as_view(), name='valor_compra'),
    ]