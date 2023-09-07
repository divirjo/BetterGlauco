import django_tables2 as tables
from BetterGlauco.tabelas_formatacao import ColunaNumericaDecimal
from .models import Ativo, InstituicaoFinanceira
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares

'''
Informações:
https://enzircle.com/responsive-table-with-django-and-htmx

https://github.com/jieter/django-tables2

https://django-tables2.readthedocs.io/

'''

CSS_PADRAO = {
                "table":{
                    "class":"min-w-full"
                },
                "thead":{
                    "class":"bg-amber-900 border-b"
                    },
                "th":{
                    "class":"text-sm font-medium text-white px-6 py-4 text-left"
                    },
                "td":{
                    "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    },
                 }

CSS_LINK = {
                "td":{
                    "class":"text-center text-dark font-medium text-base py-3 px-2" 
                    },
                "a":{
                    "class":"border border-amber-900 rounded-md py-1 px-4 text-amber-900 inline-block rounded hover:bg-amber-900 hover:text-white" 
                    },
                 }


class TabelaAtivos (tables.Table):
    
    desdobramento = ColunaNumericaDecimal(accessor="desdobramento",
                                          verbose_name="Desdobramento BRD")
    cnpj = tables.Column(verbose_name="CNPJ")
    
    editar = tables.LinkColumn('investimento:config_ativo_editar',
                               text='atualizar', 
                               args=[tables.utils.A('pk')], 
                               orderable=False,
                               empty_values=(),
                               attrs=CSS_LINK) 
    

#    def render_desdobramento(self, value, column):
#        column.attrs.update({"td":{'style':'text-align: right;'}})
#        return '{:0.2f}'.format(value)
    
    class Meta:
        model = Ativo
        attrs = CSS_PADRAO
 
 
class TabelaInstituicaoFinanceira (tables.Table):
       
    editar = tables.LinkColumn('investimento:config_instituicao_financeira_editar',
                               text='atualizar', 
                               args=[tables.utils.A('pk')], 
                               orderable=False,
                               empty_values=(),
                               attrs=CSS_LINK) 
    
    class Meta:
        model = InstituicaoFinanceira
        attrs = CSS_PADRAO


class Tabela_brd_dividendos_impostos(tables.Table):
    valor_dividendo = tables.Column()
    valor_dividendo.verbose_name = 'Dividendos recebidos (R$)'
    
    valor_impostos = tables.Column()
    valor_impostos.verbose_name = 'Impostos USA estimados (R$)'
    
    class Meta:
        template_name = 'tables/semantic.html'
       
    
  
