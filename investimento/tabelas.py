import django_tables2 as tables

from BetterGlauco.tabelas_formatacao import (
    ColunaDinheiro,
    ColunaNumericaDecimal,
    ColunaSomaNumericaDecimal,
    ParametrosTabelas,
)

from .models import (
    Ativo,
    AtivoPerfilCaixa,
    Caixa,
    ClasseAtivo,
    InstituicaoFinanceira,
)

"""
Informações:
https://enzircle.com/responsive-table-with-django-and-htmx

https://github.com/jieter/django-tables2

https://django-tables2.readthedocs.io/

"""


class TabelaAtivos(tables.Table):
    desdobramento = ColunaNumericaDecimal(
        accessor='desdobramento', verbose_name='Desdobramento BDR'
    )
    cnpj = tables.Column(verbose_name='CNPJ')

    editar = tables.LinkColumn(
        'invest_alocacao:config_ativo_editar',
        text='atualizar',
        args=[tables.utils.A('pk')],
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK,
    )

    #    def render_desdobramento(self, value, column):
    #        column.attrs.update({"td":{'style':'text-align: right;'}})
    #        return '{:0.2f}'.format(value)

    class Meta:
        model = Ativo
        attrs = ParametrosTabelas.CSS_PADRAO


class TabelaAlocacaoAtivos(tables.Table):
    subclasse = tables.Column(verbose_name='Subclasse')

    ativo = tables.Column(verbose_name='Ativo')

    alocacao_teorica_valor = ColunaDinheiro(
        verbose_name='Valor alocação teórica (R$)'
    )

    aloc_teor_percent_caixa = ColunaSomaNumericaDecimal(
        verbose_name='Percentual alocação teórica (%) Caixa'
    )

    aloc_teor_percent_carteira = ColunaSomaNumericaDecimal(
        verbose_name='Percentual alocação teórica (%) Carteira'
    )

    editar = tables.LinkColumn(
        'invest_alocacao:config_ativo_alocacao_editar',
        text='atualizar',
        args=[tables.utils.A('pk')],
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK,
    )

    class Meta:
        model = AtivoPerfilCaixa
        attrs = ParametrosTabelas.CSS_PADRAO


class Tabela_bdr_dividendos_impostos(tables.Table):
    valor_dividendo = tables.Column()
    valor_dividendo.verbose_name = 'Dividendos recebidos (R$)'

    valor_impostos = tables.Column()
    valor_impostos.verbose_name = 'Impostos USA estimados (R$)'

    class Meta:
        template_name = 'tables/semantic.html'


class TabelaCaixas(tables.Table):
    nome = tables.Column(verbose_name='Caixa', footer='Total:')

    cota_sistema_valor = ColunaDinheiro(verbose_name='Valor cota (R$)')

    alocacao_teorica_valor = ColunaDinheiro(
        verbose_name='Valor alocação teórica (R$)'
    )

    alocacao_teorica_percentual = ColunaSomaNumericaDecimal(
        verbose_name='Percentual alocação teórica (%)'
    )

    editar = tables.LinkColumn(
        'invest_alocacao:config_caixa_editar',
        text='atualizar',
        args=[tables.utils.A('pk')],
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK,
    )

    class Meta:
        model = Caixa
        attrs = ParametrosTabelas.CSS_PADRAO


class TabelaClasseAtivo(tables.Table):
    nome = tables.Column(
        verbose_name='Classe Ativo',
    )

    caixa = tables.Column(
        verbose_name='Caixa',
    )

    alocacao_teorica_valor = ColunaDinheiro(
        verbose_name='Valor alocação teórica (R$)'
    )

    alocacao_teorica_percentual = ColunaSomaNumericaDecimal(
        verbose_name='Percentual alocação teórica (%)'
    )

    subtotal = tables.Column(verbose_name='Subtotal')

    editar = tables.LinkColumn(
        'invest_alocacao:config_classe_ativo_editar',
        text='atualizar',
        args=[tables.utils.A('pk')],
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK,
    )
    """
    def render_subtotal(self, record):
        # Calcula o subtotal para cada categoria
        subtotal = AtivoPerfilCaixa.objects.filter(caixa=self.caixa).aggregate(
            Sum('alocacao_teorica_percentual')
        )['alocacao_teorica_percentual__sum']
        self.subtotal = subtotal
        return subtotal
    """

    class Meta:
        model = ClasseAtivo
        attrs = ParametrosTabelas.CSS_PADRAO


class TabelaInstituicaoFinanceira(tables.Table):
    editar = tables.LinkColumn(
        'invest_alocacao:config_instituicao_financeira_editar',
        text='atualizar',
        args=[tables.utils.A('pk')],
        orderable=False,
        empty_values=(),
        attrs=ParametrosTabelas.CSS_LINK,
    )

    class Meta:
        model = InstituicaoFinanceira
        attrs = ParametrosTabelas.CSS_PADRAO
