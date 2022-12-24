from django.contrib.auth import views as auth_view
from django.urls import path
from .views import HomeInvestimento


app_name='investimento'

urlpatterns = [
    path('inicio/', HomeInvestimento.as_view(), name='home_investimento'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    ]