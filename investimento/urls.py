from django.urls import path
from .views import HomeInvestimento


app_name='investimento'

urlpatterns = [
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    ]