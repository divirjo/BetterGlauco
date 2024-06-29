from django.urls import path

from .views import (
    InicioOperacao,
    OperacaoIndividual,
    OperacaoIndividualBolsaNova,
    OperacaoIndividualEditar,
    OperacaoIndividualFundoNova,
    RegistraNotaCorretagem,
)

app_name = 'invest_operacao'

urlpatterns = [
    path('', InicioOperacao.as_view(), name='inicio_operacao'),
    path(
        'nota_corretora/',
        RegistraNotaCorretagem.as_view(),
        name='nota_corretagem',
    ),
    path(
        'nota_corretora/<int:id_linha>',
        RegistraNotaCorretagem.as_view(),
        name='nota_corretagem',
    ),
    path(
        'individual/', OperacaoIndividual.as_view(), name='operacao_individual'
    ),
    path(
        'individual/bolsa/novo/',
        OperacaoIndividualBolsaNova.as_view(),
        name='operacao_individual_bolsa_nova',
    ),
    path(
        'individual/fundo/novo/',
        OperacaoIndividualFundoNova.as_view(),
        name='operacao_individual_fundo_nova',
    ),
    path(
        'individual/editar/<int:pk>',
        OperacaoIndividualEditar.as_view(),
        name='operacao_individual_editar',
    ),
]
