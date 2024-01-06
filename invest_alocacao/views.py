from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import redirect
import django_tables2 as tables2 
from django.views.generic import FormView, TemplateView, UpdateView
from .filtros import FiltroAtivo, FiltroClasseAtivo
from .forms import FormAtivo, \
                    FormAtivoPerfilCaixa, \
                    FormCaixa, \
                    FormClasseAtivo,\
                    FormInstituicaoFinanceira
from investimento.models import Ativo, \
                                AtivoPerfilCaixa, \
                                Caixa, \
                                ClasseAtivo, \
                                InstituicaoFinanceira
from investimento.tabelas import TabelaAtivos, \
                                    TabelaCaixas, \
                                    TabelaClasseAtivo, \
                                    TabelaInstituicaoFinanceira
from .tabela_alocacao import TabelaAlocacao
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class InicioAlocacao(LoginRequiredMixin, TemplateView):
    template_name = 'alocacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        tabela = TabelaAlocacao(context['id_perfil_selecionado'])
        context['tabela'] = tabela.getTabelaAlocacaoTeorica()
        return context 

class ConfiguracaoMenu(LoginRequiredMixin, TemplateView):
    template_name = 'configuracao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 


class ConfigurarAtivo(LoginRequiredMixin, tables2.SingleTableMixin, FilterView):
    filterset_class = FiltroAtivo
    queryset = Ativo.objects.order_by('ticket','nome')
    model = Ativo
    table_class = TabelaAtivos
    template_name = 'configuracao_filtrar_tabela.html'

       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Ativos Cadastrados'
        context['nome_parametro'] = 'ativo'
        context['url_insert'] = 'invest_alocacao:config_ativo_novo'
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
        return redirect('invest_alocacao:config_ativos')
    
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
        return redirect('invest_alocacao:config_ativos')


class ConfigurarAtivoAlocacao(LoginRequiredMixin, TemplateView):
    template_name = 'alocacao_teorica_completa.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Ativos: cadastrar alocação'
        context['nome_parametro'] = 'alocacao ativo'
        context['url_insert'] = 'invest_alocacao:config_ativo_alocacao_novo'
        context['url_edit'] = 'invest_alocacao:config_ativo_alocacao_editar'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        tabela = TabelaAlocacao(context['id_perfil_selecionado'])
        context['tabela'] = tabela.getTabelaAlocacaoTeorica()
        return context 


class ConfigurarAtivoAlocacaoNovo(LoginRequiredMixin, FormView):
    form_class = FormAtivoPerfilCaixa
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'alocacao ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['form'].fields['subclasse'].queryset = ClasseAtivo.objects.filter(caixa__perfil=context['id_perfil_selecionado'])
        context['form'].fields['corretora'].queryset = InstituicaoFinanceira.objects.filter(perfil=context['id_perfil_selecionado'])
        context['form'].fields['ativo'].queryset = Ativo.objects.order_by('ticket','nome')
        return context
       
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Alocação do ativo cadastrada com sucesso')
        return redirect('invest_alocacao:config_ativos_alocacao')    

class ConfigurarAtivoAlocacaoEditar(LoginRequiredMixin, UpdateView):
    form_class = FormAtivoPerfilCaixa
    model = AtivoPerfilCaixa
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'alocação ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['form'].fields['subclasse'].queryset = ClasseAtivo.objects.filter(caixa__perfil=context['id_perfil_selecionado'])
        context['form'].fields['corretora'].queryset = InstituicaoFinanceira.objects.filter(perfil=context['id_perfil_selecionado'])
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Alocação do ativo atualizada com sucesso')
        return redirect('invest_alocacao:config_ativos_alocacao')  


class ConfigurarCaixa(LoginRequiredMixin, tables2.SingleTableView):
    table_class = TabelaCaixas
    template_name = 'configuracao_listar_tabela.html'
    
    
    def get_queryset(self, **kwargs):
        return Caixa.objects.filter(
                    perfil_id = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)).order_by('ordem_exibicao','nome')
           
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Caixas: Alocação por classe de ativo'
        context['nome_parametro'] = 'caixa'
        context['url_insert'] = 'invest_alocacao:config_caixa_novo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 

class ConfigurarCaixaNovo(LoginRequiredMixin, FormView):
    form_class = FormCaixa
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'caixa'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Caixa cadastrada com sucesso')
        return redirect('invest_alocacao:config_ativos_alocacao')
    
class ConfigurarCaixaEditar(LoginRequiredMixin, UpdateView):
    form_class = FormCaixa
    model = Caixa
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'caixa'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Caixa atualizada com sucesso')
        return redirect('invest_alocacao:config_caixa')  

class ConfigurarSubCaixa(LoginRequiredMixin, tables2.SingleTableMixin, FilterView):
    table_class = TabelaClasseAtivo
    model = ClasseAtivo
    filterset_class = FiltroClasseAtivo
    template_name = 'configuracao_filtrar_tabela.html'
     
    
    def get_filterset(self, *args, **kwargs):
        fs = super().get_filterset(*args, **kwargs)
        fs.filters['caixa'].field.queryset = fs.filters['caixa'].field.queryset.filter(perfil_id=self.request.session['id_perfil_selecionado']).order_by('ordem_exibicao','nome')
        return fs
    
    def get_queryset(self, **kwargs):
        return ClasseAtivo.objects.filter(
                    caixa__perfil_id = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)).order_by('caixa__ordem_exibicao','caixa__nome','nome')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Sub Caixas: alocação por classe de ativo'
        context['nome_parametro'] = 'classe ativo'
        context['url_insert'] = 'invest_alocacao:config_classe_ativo_novo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    
    def montaTabelaCaixas(query):
        return query
        

class ConfigurarSubCaixaNovo(LoginRequiredMixin, FormView):
    form_class = FormClasseAtivo
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'classe ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['form'].fields['caixa'].queryset = Caixa.objects.filter(perfil=context['id_perfil_selecionado'])

        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Classe de ativo cadastrada com sucesso')
        return redirect('invest_alocacao:config_classe_ativo')
    
class ConfigurarSubCaixaEditar(LoginRequiredMixin, UpdateView):
    form_class = FormClasseAtivo
    model = ClasseAtivo
    template_name = 'configuracao_editar_tabela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_parametro'] = 'classe ativo'
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['form'].fields['caixa'].queryset = Caixa.objects.filter(perfil=context['id_perfil_selecionado'])
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        caixa = form.save(commit=False)
        caixa.perfil_id = context['id_perfil_selecionado']
        caixa.save() 
        messages.success(self.request, 'Classe ativo atualizada com sucesso')
        return redirect('invest_alocacao:config_classe_ativo')  


class ConfigurarInstituicaoFinanceira(LoginRequiredMixin, tables2.SingleTableView):
    table_class = TabelaInstituicaoFinanceira
    template_name = 'configuracao_listar_tabela.html'
    
    
    def get_queryset(self, **kwargs):
        return InstituicaoFinanceira.objects.filter(
                    perfil_id = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)).order_by('nome')
           
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Instituições Financeiras Cadastradas'
        context['nome_parametro'] = 'instituição financeira'
        context['url_insert'] ='invest_alocacao:config_instituicao_financeira_novo'
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
        return redirect('invest_alocacao:config_instituicao_financeira')
    
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
        return redirect('invest_alocacao:config_instituicao_financeira') 

