from django.urls import path

from .views import (
    Ajuda,
    HomeInvestimento,
    Imposto_bdr_usa,
    Valor_compra,
)

app_name = 'investimento'

urlpatterns = [
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    path('help/', Ajuda.as_view(), name='ajuda_inicio'),
    path(
        'imposto-dividendo-bdr/',
        Imposto_bdr_usa.as_view(),
        name='imposto_dividendo_bdr',
    ),
    path('valor-compra/', Valor_compra.as_view(), name='valor_compra'),
]
