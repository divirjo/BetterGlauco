from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import django_tables2 as tables2 
from django.views.generic import FormView, TemplateView, UpdateView
from .bdr import BDR
from BetterGlauco.parametro import Constante
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'


class Imposto_bdr_usa(LoginRequiredMixin, TemplateView):
    template_name = 'bdr_imposto_usa.html'
    _CONSTANTE = Constante()
    tabela = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs) 
        valor_dividendos = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_dividendos'))
        indice_imposto = self._CONSTANTE.BDR_IMPOSTO_DIVIDENDOS_USA()
        
        self.tabela['Dividendos recebidos (R$)'] = valor_dividendos
        imposto_retido = valor_dividendos * indice_imposto
        self.tabela['Imposto de Renda EUA retido na fonte estimado (R$)'] = imposto_retido
            
        context['tabela_resultados'] = self.tabela
        return context
        
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    calculo_bdr = {'Compra':{}, 'Venda':{}}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs) 
        bdr_ativo = BDR(self.request, self.request.GET.get('ticket'))
        if bdr_ativo.ativo_selecionado.ticket:
            self.monta_tabela_custos(bdr_ativo)
        context['calculo_bdr'] = self.calculo_bdr
        return context
    
    def monta_tabela_custos(self, bdr):
        valor_US_digitado = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_US'))       
        bdr.calcular_preco_referencia(valor_US_digitado)
        self.gera_linha_tabela('Compra',bdr)
        self.gera_linha_tabela('Venda', bdr)
    
    def gera_linha_tabela(self, operacao, bdr):
        valor_BR_digitado = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_BDR'))
        
        self.calculo_bdr[operacao]['Ticket'] = bdr.ativo_selecionado.ticket
        self.calculo_bdr[operacao]['USA'] = bdr.ativo_selecionado.ticket_original
        self.calculo_bdr[operacao]['Desdobramento'] = int(bdr.ativo_selecionado.desdobramento)
        self.calculo_bdr[operacao]['Custo BDR'] = bdr.custos_bdr
        self.calculo_bdr[operacao]['Preço (U$)'] = bdr.ticket_original_valor_us
        
        if operacao == 'Venda':
            self.calculo_bdr[operacao]['Dólar (R$)'] = bdr.dolar_compra
            self.calculo_bdr[operacao]['Preço referência (R$)'] = '{:.2f}'.format(bdr.preco_referencia_venda)
        else:
            self.calculo_bdr[operacao]['Dólar (R$)'] = bdr.dolar_venda
            self.calculo_bdr[operacao]['Preço referência (R$)'] = '{:.2f}'.format(bdr.preco_referencia_compra)
        
        self.calculo_bdr[operacao]['Preço atual (R$)'] = '{:.2f}'.format(valor_BR_digitado)
        if bdr.preco_referencia_compra == 0:
            spread = 0
        else:
            spread = (valor_BR_digitado / bdr.preco_referencia_compra) - 1
        self.calculo_bdr[operacao]['Spread'] = '{:.2%}'.format(spread)
    
    

    

    

        
            

    
