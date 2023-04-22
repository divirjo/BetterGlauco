from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import django_tables2 as tables2 
from django.views.generic import FormView, TemplateView
from .brd import BRD
from .models import Ativo
from .tabelas import TabelaAtivos
from BetterGlauco.parametro import Constante
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares

class Auxiliar():

    def get_perfil_ativo(request, **kwargs):
        if request.GET.get('perfil'):
            id_perfil = Funcoes_auxiliares.converte_numero_str(request.GET.get('perfil')) 
        else:
            id_perfil = kwargs.get('id_perfil', 0) 
        return id_perfil


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs)
        return context  


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'


class ConfiguracaoMenu(LoginRequiredMixin, TemplateView):
    template_name = 'configuracao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs)
        return context 


class ConfigurarAtivo(LoginRequiredMixin, tables2.SingleTableView):
    table_class = TabelaAtivos
    queryset = Ativo.objects.all()
    template_name = 'config_ativos_listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs)
        messages.warning(self.request, 'Cadastro geral. Alterações aqui afetarão todos os usuários do sistema')

        return context 
    
class ConfigurarAtivoEditar(LoginRequiredMixin, TemplateView):
    template_name = 'configuracao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs)
        
        
        return context 

class Imposto_brd_usa(LoginRequiredMixin, TemplateView):
    template_name = 'brd_imposto_usa.html'
    _CONSTANTE = Constante()
    tabela = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs) 
        valor_dividendos = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_dividendos'))
        indice_imposto = self._CONSTANTE.BRD_IMPOSTO_DIVIDENDOS_USA()
        
        self.tabela['Dividendos recebidos (R$)'] = valor_dividendos
        imposto_retido = valor_dividendos * indice_imposto
        self.tabela['Imposto de Renda EUA retido na fonte estimado (R$)'] = imposto_retido
            
        context['tabela_resultados'] = self.tabela
        return context
        
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    calculo_brd = {'Compra':{}, 'Venda':{}}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_ativo_id'] = Auxiliar.get_perfil_ativo(self.request, **kwargs) 
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
    
    

    

    

        
            

    
