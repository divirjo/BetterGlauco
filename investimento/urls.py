from django.urls import path
from .views import Ajuda, ConfiguracaoMenu, ConfigurarAtivo, ConfigurarAtivoNovo, ConfigurarAtivoEditar, HomeInvestimento, Imposto_brd_usa, Valor_compra


app_name='investimento'

urlpatterns = [
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    path('config/', ConfiguracaoMenu.as_view(), name='configuracao'),
    path('config/ativos/', ConfigurarAtivo.as_view(), name='config_ativos'),
    path('config/ativos/novo/', ConfigurarAtivoNovo.as_view(), name='config_ativos_novo'),
    path('config/ativos/editar/<int:pk>', ConfigurarAtivoEditar.as_view(), name='config_ativos_editar'),
    path('help/', Ajuda.as_view(), name='ajuda_inicio'),
    path('imposto-dividendo-brd/', Imposto_brd_usa.as_view(), name='imposto_dividendo_brd'),
    path('valor-compra/', Valor_compra.as_view(), name='valor_compra'),
    ]