from django.urls import path
from .views import InicioAtualizacao, \
                    PosicaoCorretora, \
                    PosicaoCorretoraNova, \
                    PosicaoCorretoraEditar, \
                    PosicaoIndividual, \
                    PosicaoIndividualNova, \
                    PosicaoIndividualEditar



app_name='invest_atualizacao'

urlpatterns = [
     path('', 
         InicioAtualizacao.as_view(), 
         name='inicio_atualizacao'),
     
     path('corretora/', 
         PosicaoCorretora.as_view(), 
         name='posicao_corretora'),
     path('corretora/novo/', 
         PosicaoCorretoraNova.as_view(), 
         name='posicao_corretora_nova'),
     path('corretora/editar/<int:pk>', 
         PosicaoCorretoraEditar.as_view(), 
         name='posicao_corretora_editar'),
     
     path('individual/', 
         PosicaoIndividual.as_view(), 
         name='posicao_individual'),
     path('individual/novo/', 
         PosicaoIndividualNova.as_view(), 
         name='posicao_individual_nova'),
     path('individual/editar/<int:pk>', 
         PosicaoIndividualEditar.as_view(), 
         name='posicao_individual_editar'),
    
    ]
