from investimento.models import ExtratoOperacao, TipoOperacao
from django.db.models import Sum

class CotasAtivo():
    
    def total(self, ativo):
        
        total_adquirido = ExtratoOperacao.objects \
            .filter(
                ativo_perfil_caixa__ativo_id=ativo
            ).exclude(operacao=TipoOperacao.VENDA) \
            .aggregate(Sum('quantidade'))
            
        total_vendido = ExtratoOperacao.objects \
            .filter(
                ativo_perfil_caixa__ativo_id=ativo,
                operacao=TipoOperacao.VENDA
            ).aggregate(Sum('quantidade'))
            
        saldo_cotas = total_adquirido['quantidade__sum'] - \
            total_vendido['quantidade__sum'] 
        return  saldo_cotas