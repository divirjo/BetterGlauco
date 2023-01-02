from django.urls import path
from .views import Ajuda, HomeInvestimento


app_name='investimento'

urlpatterns = [
    path('help/', Ajuda.as_view(), name='ajuda_inicio'),
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    ]