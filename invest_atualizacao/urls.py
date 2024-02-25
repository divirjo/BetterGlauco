from django.urls import path
from .views import InicioAtualizacao, \
    DividendosInicio, DividendoNovo, DividendoEditar, \
    PosicaoIndividualBolsa, PosicaoIndividualBolsaNova, \
    PosicaoIndividualBolsaEditar, \
    PosicaoIndividualFundo, PosicaoIndividualFundoNova, \
    PosicaoIndividualFundoEditar



app_name='invest_atualizacao'

urlpatterns = [
    path('', 
        InicioAtualizacao.as_view(), 
        name='inicio_atualizacao'),
     
    path('dividendos/', 
        DividendosInicio.as_view(), 
        name='dividendos'),
    path('dividendos/novo/', 
        DividendoNovo.as_view(), 
        name='dividendos_novo'),
    path('dividendos/editar/<int:pk>', 
        DividendoEditar.as_view(), 
        name='dividendos_editar'), 

    path('individual/bolsa/', 
        PosicaoIndividualBolsa.as_view(), 
        name='posicao_individual_bolsa'),
    path('individual/bolsa/novo/', 
        PosicaoIndividualBolsaNova.as_view(), 
        name='posicao_individual_bolsa_nova'),
    path('individual/bolsa/editar/<int:pk>', 
        PosicaoIndividualBolsaEditar.as_view(), 
        name='posicao_individual_bolsa_editar'),  
     
    path('individual/fundo/', 
        PosicaoIndividualFundo.as_view(), 
        name='posicao_individual_fundo'),
    path('individual/fundo/novo/', 
        PosicaoIndividualFundoNova.as_view(), 
        name='posicao_individual_fundo_nova'),
    path('individual/fundo/editar/<int:pk>', 
        PosicaoIndividualFundoEditar.as_view(), 
        name='posicao_individual_fundo_editar'),    

]
