import django_tables2 as tables

from BetterGlauco.tabelas_formatacao import ColunaData, \
    ColunaNumericaDecimal, ColunaSomaNumericaDecimal, ColunaDinheiro, \
    ColunaSomaDinheiro, ParametrosTabelas
from investimento.models import PosicaoDataFundo, PosicaoDataBolsa


class TabelaPosicaoBolsa(tables.Table):
    
    editar = tables.LinkColumn(
        'invest_atualizacao:posicao_individual_bolsa_editar',
        text='atualizar', 
        args=[tables.utils.A('pk')], 
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK
    ) 
    
    class Meta:
        model = PosicaoDataBolsa
        attrs = ParametrosTabelas.CSS_PADRAO


class TabelaPosicaoFundos(tables.Table):
    
    cota_sistema_valor = ColunaDinheiro(verbose_name="Valor cota (R$)")
    cota_valor_dolar = ColunaDinheiro(verbose_name="Valor cota (US$)")
    cotas = ColunaNumericaDecimal()
    total = ColunaDinheiro(verbose_name="Total (R$)")
    
    editar = tables.LinkColumn(
        'invest_atualizacao:posicao_individual_fundo_editar',
        text='atualizar', 
        args=[tables.utils.A('pk')], 
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK
    ) 
    
    
    class Meta:
        model = PosicaoDataFundo
        attrs = ParametrosTabelas.CSS_PADRAO
        
        