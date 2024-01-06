import django_tables2 as tables

from BetterGlauco.tabelas_formatacao import ColunaData, \
                                        ColunaNumericaDecimal, \
                                        ColunaSomaNumericaDecimal, \
                                        ColunaDinheiro, \
                                        ColunaSomaDinheiro, \
                                        ParametrosTabelas
from investimento.models import PosicaoData

class TabelaPosicaoAtivos(tables.Table):
    
    editar = tables.LinkColumn('invest_atualizacao:posicao_individual_editar',
                               text='atualizar', 
                               args=[tables.utils.A('pk')], 
                               orderable=False,
                               empty_values=(),
                               attrs=ParametrosTabelas.CSS_LINK) 
    
    class Meta:
        model = PosicaoData
        attrs = ParametrosTabelas.CSS_PADRAO