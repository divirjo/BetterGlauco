from django.urls import path
from .views import Ajuda,\
                    ConfiguracaoMenu, \
                    ConfigurarAtivo, \
                    ConfigurarAtivoNovo, \
                    ConfigurarAtivoEditar, \
                    ConfigurarCaixa, \
                    ConfigurarCaixaNovo, \
                    ConfigurarCaixaEditar, \
                    ConfigurarInstituicaoFinanceira, \
                    ConfigurarInstituicaoFinanceiraEditar, \
                    ConfigurarInstituicaoFinanceiraNovo, \
                    HomeInvestimento, \
                    Imposto_brd_usa, \
                    Valor_compra


app_name='investimento'

urlpatterns = [
    path('', 
         HomeInvestimento.as_view(), 
         name='home_investimento'),
    path('config/', 
         ConfiguracaoMenu.as_view(), 
         name='configuracao'),
    path('config/ativo/', 
         ConfigurarAtivo.as_view(), 
         name='config_ativos'),
    path('config/ativo/novo/', 
         ConfigurarAtivoNovo.as_view(), 
         name='config_ativo_novo'),
    path('config/ativo/editar/<int:pk>', 
         ConfigurarAtivoEditar.as_view(), 
         name='config_ativo_editar'),
    path('config/caixa/', 
         ConfigurarCaixa.as_view(),
         name='config_caixa'),
    path('config/caixa/novo/',
         ConfigurarCaixaNovo.as_view(),
         name='config_caixa_novo'),
    path('config/caixa/editar/<int:pk>',
         ConfigurarCaixaEditar.as_view(),
         name='config_caixa_editar'),
    path('config/instituicao_financeira/', 
         ConfigurarInstituicaoFinanceira.as_view(),
         name='config_instituicao_financeira'),
    path('config/instituicao_financeira/novo/',
         ConfigurarInstituicaoFinanceiraNovo.as_view(),
         name='config_instituicao_financeira_novo'),
    path('config/instituicao_financeira/editar/<int:pk>',
         ConfigurarInstituicaoFinanceiraEditar.as_view(),
         name='config_instituicao_financeira_editar'),
    path('help/', 
         Ajuda.as_view(), 
         name='ajuda_inicio'),
    path('imposto-dividendo-brd/', 
         Imposto_brd_usa.as_view(), 
         name='imposto_dividendo_brd'),
    path('valor-compra/', 
         Valor_compra.as_view(), 
         name='valor_compra'),
    ]