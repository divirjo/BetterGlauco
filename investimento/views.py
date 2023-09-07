from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import django_tables2 as tables2 
from django.views.generic import FormView, TemplateView, UpdateView
from .brd import BRD
from .forms import FormAtivo, FormInstituicaoFinanceira
from .models import Ativo, InstituicaoFinanceira
from .tabelas import TabelaAtivos, TabelaInstituicaoFinanceira
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


class ConfiguracaoMenu(LoginRequiredMixin, TemplateView):
    template_name = 'configuracao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 


class ConfigurarAtivo(LoginRequiredMixin, tables2.SingleTableView):
    table_class = TabelaAtivos
    queryset = Ativo.objects.all()
    template_name = 'configuracao_listar_tabela.html'

       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Ativos Cadastrados'
        context['nome_parametro'] = 'ativo'
        context['url_insert'] = 'investimento:config_ativo_novo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        messages.warning(self.request, 'Cadastro geral. Alterações aqui afetarão todos os usuários do sistema ')
        return context 

class ConfigurarAtivoNovo(LoginRequiredMixin, FormView):
    form_class = FormAtivo
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        messages.warning(self.request, 'Cadastro geral. Alterações aqui afetarão todos os usuários do sistema')
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        form.save() # insere o item no BD
        messages.success(self.request, 'Ativo incluído com sucesso')
        return redirect('investimento:config_ativos')
    
class ConfigurarAtivoEditar(LoginRequiredMixin, UpdateView):
    form_class = FormAtivo
    model = Ativo
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        messages.warning(self.request, 'Cadastro geral. Alterações aqui afetarão todos os usuários do sistema')
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        form.save() # insere o item no BD
        messages.success(self.request, 'Ativo alterado com sucesso')
        return redirect('investimento:config_ativos')

class ConfigurarInstituicaoFinanceira(LoginRequiredMixin, tables2.SingleTableView):
    table_class = TabelaInstituicaoFinanceira
    template_name = 'configuracao_listar_tabela.html'
    
    
    def get_queryset(self, **kwargs):
        return InstituicaoFinanceira.objects.filter(
                    perfil_id = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs))
           
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Instituições Financeiras Cadastradas'
        context['nome_parametro'] = 'instituição financeira'
        context['url_insert'] = 'investimento:config_instituicao_financeira_novo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 

class ConfigurarInstituicaoFinanceiraNovo(LoginRequiredMixin, FormView):
    form_class = FormInstituicaoFinanceira
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'instituição financeira'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        instituicao_financeira = form.save(commit=False)
        instituicao_financeira.perfil_id = context['id_perfil_selecionado']
        instituicao_financeira.save() 
        messages.success(self.request, 'Instituição incluída com sucesso')
        return redirect('investimento:config_instituicao_financeira')
    
class ConfigurarInstituicaoFinanceiraEditar(LoginRequiredMixin, UpdateView):
    form_class = FormInstituicaoFinanceira
    model = InstituicaoFinanceira
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'instituição financeira'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        instituicao_financeira = form.save(commit=False)
        instituicao_financeira.perfil_id = context['id_perfil_selecionado']
        instituicao_financeira.save() 
        form.save() 
        messages.success(self.request, 'Instituição alterada com sucesso')
        return redirect('investimento:config_instituicao_financeira')   

class Imposto_brd_usa(LoginRequiredMixin, TemplateView):
    template_name = 'brd_imposto_usa.html'
    _CONSTANTE = Constante()
    tabela = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs) 
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
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs) 
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
    
    

    

    

        
            

    
