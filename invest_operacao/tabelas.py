import django_tables2 as tables
from django_tables2.utils import A
from django.db.models import Sum
from investimento.models import ExtratoOperacao
from BetterGlauco.tabelas_formatacao import ColunaData, \
                                        ColunaNumericaDecimal, \
                                        ColunaSomaNumericaDecimal, \
                                        ColunaDinheiro, \
                                        ParametrosTabelas
                                        
                                        

class TabelaExtratoOperacoes(tables.Table):
           
    ativo_perfil_caixa = tables.Column(verbose_name='Ativo')
    
    custos_transacao = ColunaDinheiro(verbose_name="Custos transação (R$)")
    
    data = ColunaData()
    
    ir_fonte = ColunaDinheiro(verbose_name="IR fonte (R$)")
    
    quantidade = ColunaNumericaDecimal()
    
    operacao = tables.Column(verbose_name='Operação')
    
    total = ColunaDinheiro(accessor=A('total'), verbose_name="Total (R$)")
    
    valor_unitario = ColunaDinheiro(verbose_name="Valor unitário (R$)")
    
    editar = tables.LinkColumn('invest_operacao:operacao_individual_editar',
                               text='atualizar', 
                               args=[tables.utils.A('pk')], 
                               orderable=False,
                               empty_values=(),
                               attrs=ParametrosTabelas.CSS_LINK) 

    
    
    class Meta:
        model = ExtratoOperacao
        attrs = ParametrosTabelas.CSS_PADRAO
        fields = ('ativo_perfil_caixa', 
                    'data',
                    'operacao',
                    'quantidade',
                    'valor_unitario',
                    'custos_transacao',
                    'ir_fonte')
        sequence = ('ativo_perfil_caixa', 
                    'data',
                    'operacao',
                    'quantidade',
                    'valor_unitario',
                    'custos_transacao',
                    'total',
                    'ir_fonte',
                    'editar')