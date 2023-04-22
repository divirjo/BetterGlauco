from django.urls import path
from .views import Ajuda, ConfiguracaoMenu, ConfigurarAtivo, ConfigurarAtivoEditar, HomeInvestimento, Imposto_brd_usa, Valor_compra


app_name='investimento'

urlpatterns = [
    path('', HomeInvestimento.as_view(), name='home_investimento'),
    path('<int:id_perfil>', HomeInvestimento.as_view(), name='home_investimento'),
    path('config/<int:id_perfil>', ConfiguracaoMenu.as_view(), name='configuracao'),
    path('config/ativos/<int:id_perfil>', ConfigurarAtivo.as_view(), name='config_ativos'),
    path('config/ativos/editar<int:id_perfil>', ConfigurarAtivoEditar.as_view(), name='config_ativos_edicao'),
    path('help/', Ajuda.as_view(), name='ajuda_inicio'),
    path('imposto-dividendo-brd/<int:id_perfil>', Imposto_brd_usa.as_view(), name='imposto_dividendo_brd'),
    path('valor-compra/<int:id_perfil>', Valor_compra.as_view(), name='valor_compra'),
    ]