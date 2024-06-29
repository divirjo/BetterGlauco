from django.urls import path

from .views import (
    ConfiguracaoMenu,
    ConfigurarAtivo,
    ConfigurarAtivoAlocacao,
    ConfigurarAtivoAlocacaoEditar,
    ConfigurarAtivoAlocacaoNovo,
    ConfigurarAtivoEditar,
    ConfigurarAtivoNovo,
    ConfigurarCaixa,
    ConfigurarCaixaEditar,
    ConfigurarCaixaNovo,
    ConfigurarInstituicaoFinanceira,
    ConfigurarInstituicaoFinanceiraEditar,
    ConfigurarInstituicaoFinanceiraNovo,
    ConfigurarSubCaixa,
    ConfigurarSubCaixaEditar,
    ConfigurarSubCaixaNovo,
    InicioAlocacao,
)

app_name = 'invest_alocacao'

urlpatterns = [
    path('', InicioAlocacao.as_view(), name='inicio_alocacao'),
    path('config/', ConfiguracaoMenu.as_view(), name='configuracao'),
    path('config/ativo/', ConfigurarAtivo.as_view(), name='config_ativos'),
    path(
        'config/ativo/novo/',
        ConfigurarAtivoNovo.as_view(),
        name='config_ativo_novo',
    ),
    path(
        'config/ativo/editar/<int:pk>',
        ConfigurarAtivoEditar.as_view(),
        name='config_ativo_editar',
    ),
    path(
        'config/ativo_alocacao/',
        ConfigurarAtivoAlocacao.as_view(),
        name='config_ativos_alocacao',
    ),
    path(
        'config/ativo_alocacao/novo/',
        ConfigurarAtivoAlocacaoNovo.as_view(),
        name='config_ativo_alocacao_novo',
    ),
    path(
        'config/ativo_alocacao/editar/<int:pk>',
        ConfigurarAtivoAlocacaoEditar.as_view(),
        name='config_ativo_alocacao_editar',
    ),
    path('config/caixa/', ConfigurarCaixa.as_view(), name='config_caixa'),
    path(
        'config/caixa/novo/',
        ConfigurarCaixaNovo.as_view(),
        name='config_caixa_novo',
    ),
    path(
        'config/caixa/editar/<int:pk>',
        ConfigurarCaixaEditar.as_view(),
        name='config_caixa_editar',
    ),
    path(
        'config/classe_ativo/',
        ConfigurarSubCaixa.as_view(),
        name='config_classe_ativo',
    ),
    path(
        'config/classe_ativo/novo/',
        ConfigurarSubCaixaNovo.as_view(),
        name='config_classe_ativo_novo',
    ),
    path(
        'config/classe_ativo/editar/<int:pk>',
        ConfigurarSubCaixaEditar.as_view(),
        name='config_classe_ativo_editar',
    ),
    path(
        'config/instituicao_financeira/',
        ConfigurarInstituicaoFinanceira.as_view(),
        name='config_instituicao_financeira',
    ),
    path(
        'config/instituicao_financeira/novo/',
        ConfigurarInstituicaoFinanceiraNovo.as_view(),
        name='config_instituicao_financeira_novo',
    ),
    path(
        'config/instituicao_financeira/editar/<int:pk>',
        ConfigurarInstituicaoFinanceiraEditar.as_view(),
        name='config_instituicao_financeira_editar',
    ),
]
