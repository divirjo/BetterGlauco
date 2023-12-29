from django.urls import path
from .views import InicioOperacao, \
                    OperacaoIndividual, \
                    OperacaoIndividualNova, \
                    OperacaoIndividualEditar \


app_name='invest_operacao'

urlpatterns = [
    path('', 
         InicioOperacao.as_view(), 
         name='inicio_operacao'),
     
     
     path('individual/', 
         OperacaoIndividual.as_view(), 
         name='operacao_individual'),
    path('individual/novo/', 
         OperacaoIndividualNova.as_view(), 
         name='operacao_individual_nova'),
    path('individual/editar/<int:pk>', 
         OperacaoIndividualEditar.as_view(), 
         name='operacao_individual_editar'),
    ]