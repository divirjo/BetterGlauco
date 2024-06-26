"""BetterGlauco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import include, path

from .views import Contato, Homepage, Sobre

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view(), name='homepage'),
    path('contato/', Contato.as_view(), name='contato'),
    path('invest/', include('investimento.urls', namespace='investimento')),
    path(
        'alocacao/',
        include('invest_alocacao.urls', namespace='invest_alocacao'),
    ),
    path(
        'operacao/',
        include('invest_operacao.urls', namespace='invest_operacao'),
    ),
    path(
        'atualizacao/',
        include('invest_atualizacao.urls', namespace='invest_atualizacao'),
    ),
    path(
        'login/',
        auth_view.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_view.LogoutView.as_view(template_name='logout.html'),
        name='logout',
    ),
    path('sobre/', Sobre.as_view(), name='sobre'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
