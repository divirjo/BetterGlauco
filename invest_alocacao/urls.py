from django.urls import path
from .views import ConfiguracaoMenu, \
                    ConfigurarAtivo, \
                    ConfigurarAtivoNovo, \
                    ConfigurarAtivoEditar, \
                    ConfigurarCaixa, \
                    ConfigurarCaixaNovo, \
                    ConfigurarCaixaEditar, \
                    ConfigurarSubCaixa, \
                    ConfigurarSubCaixaNovo, \
                    ConfigurarSubCaixaEditar, \
                    ConfigurarInstituicaoFinanceira, \
                    ConfigurarInstituicaoFinanceiraEditar, \
                    ConfigurarInstituicaoFinanceiraNovo \



app_name='invest_alocacao'

urlpatterns = [
    path('', 
         ConfiguracaoMenu.as_view(), 
         name='configuracao'),
     path('alocacao/', 
         ConfiguracaoMenu.as_view(), 
         name='configuracao'),
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
    
    path('config/classe_ativo/', 
         ConfigurarSubCaixa.as_view(),
         name='config_classe_ativo'),
    path('config/classe_ativo/novo/',
         ConfigurarSubCaixaNovo.as_view(),
         name='config_classe_ativo_novo'),
    path('config/classe_ativo/editar/<int:pk>',
         ConfigurarSubCaixaEditar.as_view(),
         name='config_classe_ativo_editar'),
    
    path('config/instituicao_financeira/', 
         ConfigurarInstituicaoFinanceira.as_view(),
         name='config_instituicao_financeira'),
    path('config/instituicao_financeira/novo/',
         ConfigurarInstituicaoFinanceiraNovo.as_view(),
         name='config_instituicao_financeira_novo'),
    path('config/instituicao_financeira/editar/<int:pk>',
         ConfigurarInstituicaoFinanceiraEditar.as_view(),
         name='config_instituicao_financeira_editar'),
    ]