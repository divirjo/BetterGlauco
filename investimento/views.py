from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django.views.generic import FormView, TemplateView
from .brd import BRD
from BetterGlauco.parametro import Constante
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'
    
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    calculo_brd = {'Compra':{}, 'Venda':{}}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brd_ativo = BRD(self.request, self.request.GET.get('ticket'))
        if brd_ativo.ativo_selecionado.ticket:
            self.monta_tabela_custos(brd_ativo)
        context['calculo_brd'] = self.calculo_brd
        return context
    
    def monta_tabela_custos(self, brd):
        valor_US_digitado = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_US'))

        
        brd.calcular_preco_referencia(valor_US_digitado)
        self.gera_linha_tabela('Compra',brd)
        self.gera_linha_tabela('Venda', brd)
    
    def gera_linha_tabela(self, operacao, brd):
        valor_BR_digitado = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_BRD'))
        
        self.calculo_brd[operacao]['Ticket'] = brd.ativo_selecionado.ticket
        self.calculo_brd[operacao]['USA'] = brd.ativo_selecionado.ticket_original
        self.calculo_brd[operacao]['Desdobramento'] = int(brd.ativo_selecionado.desdobramento)
        self.calculo_brd[operacao]['Custo BRD'] = brd.custos_brd
        self.calculo_brd[operacao]['Preço (U$)'] = brd.ticket_original_valor_us
        
        if operacao == 'Venda':
            self.calculo_brd[operacao]['Dólar (R$)'] = brd.dolar_compra
            self.calculo_brd[operacao]['Preço referência (R$)'] = '{:.2f}'.format(brd.preco_referencia_venda)
        else:
            self.calculo_brd[operacao]['Dólar (R$)'] = brd.dolar_venda
            self.calculo_brd[operacao]['Preço referência (R$)'] = '{:.2f}'.format(brd.preco_referencia_compra)
        
        self.calculo_brd[operacao]['Preço atual (R$)'] = '{:.2f}'.format(valor_BR_digitado)
        if brd.preco_referencia_compra == 0:
            spread = 0
        else:
            spread = (valor_BR_digitado / brd.preco_referencia_compra) - 1
        self.calculo_brd[operacao]['Spread'] = '{:.2%}'.format(spread)
    
    
class Imposto_brd_usa(LoginRequiredMixin, TemplateView):
    template_name = 'brd_imposto_usa.html'
    _CONSTANTE = Constante()
    tabela = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valor_dividendos = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_dividendos'))
        indice_imposto = self._CONSTANTE.BRD_IMPOSTO_DIVIDENDOS_USA()
        
        self.tabela['Dividendos recebidos (R$)'] = valor_dividendos
        imposto_retido = valor_dividendos * indice_imposto
        self.tabela['Imposto de Renda EUA retido na fonte estimado (R$)'] = imposto_retido
            
        context['tabela_resultados'] = self.tabela
        return context
    
    

    

        
            

    
