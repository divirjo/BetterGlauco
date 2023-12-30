from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
import django_tables2 as tables2 
from django_tables2.paginators import LazyPaginator
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, UpdateView
from .filtros_operacoes import FiltroOperacaoAtivo
from .forms_operacoes import FormExtratoOperacao
from .tabelas import TabelaExtratoOperacoes
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares
from investimento.models import AtivoPerfilCaixa, ExtratoOperacao


class InicioOperacao(LoginRequiredMixin, tables2.SingleTableView):
    paginator_class = LazyPaginator
    table_class = TabelaExtratoOperacoes
    template_name = 'operacao_inicio.html'
    
    def get_queryset(self, **kwargs):
        return ExtratoOperacao.objects.filter(
            ativo_perfil_caixa__subclasse__caixa__perfil=Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
            ).order_by('-data')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
   
   
class RegistraNotaCorretagem(LoginRequiredMixin, tables2.SingleTableView):
    template_name = 'registrar_nota_corretagem'
    
    

class OperacaoIndividual(LoginRequiredMixin, tables2.SingleTableMixin, FilterView):
    filterset_class = FiltroOperacaoAtivo
    paginator_class = LazyPaginator
    table_class = TabelaExtratoOperacoes
    template_name = 'operacao_historico_ativo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['titulo_pagina'] = 'Histórico de Operações'
        context['nome_parametro'] = 'registrar compra ou venda'
        context['url_insert'] = 'invest_operacao:operacao_individual_nova'
        return context 
    
    def get_filterset(self, *args, **kwargs):
        fs = super().get_filterset(*args, **kwargs)
        fs.filters['ativo_perfil_caixa'].field.queryset = fs.filters['ativo_perfil_caixa'].field.queryset.filter(subclasse__caixa__perfil_id=self.request.session['id_perfil_selecionado'])
        fs.filters['ativo_perfil_caixa'].field.order_by = ('ativo_perfil_caixa__ativo__ticket','ativo_perfil_caixa__ativo__nome')
        return fs
    
    def get_queryset(self, **kwargs):
        return ExtratoOperacao.objects.filter(
            ativo_perfil_caixa__subclasse__caixa__perfil=Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
            ).order_by('-data')

class OperacaoIndividualNova(LoginRequiredMixin, FormView):
    form_class = FormExtratoOperacao
    template_name = 'registrar_operacao_individual.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['nome_parametro'] = 'registrar compra ou venda'
        
        #Campo formulário
        context['form'].fields['ativo_perfil_caixa'].queryset = AtivoPerfilCaixa.objects.filter(subclasse__caixa__perfil=context['id_perfil_selecionado'])

        return context 
    
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        operacao = form.save(commit=False)
        operacao.save() 
        messages.success(self.request, 'Operação de {} cadastrada com sucesso'.format(form.cleaned_data['operacao']))
        return redirect('invest_operacao:operacao_individual')   


class OperacaoIndividualEditar(LoginRequiredMixin, UpdateView):
    form_class = FormExtratoOperacao
    model = ExtratoOperacao
    template_name = 'registrar_operacao_individual.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['nome_parametro'] = 'registrar compra ou venda'
        
        #Campo formulário
        context['form'].fields['ativo_perfil_caixa'].queryset = AtivoPerfilCaixa.objects.filter(subclasse__caixa__perfil=context['id_perfil_selecionado'])
        
        return context 
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        operacao = form.save(commit=False)
        operacao.save() 
        messages.success(self.request, 'Operação de {} atualizada com sucesso'.format(form.cleaned_data['operacao']))
        return redirect('invest_operacao:operacao_individual')   
    
    
    