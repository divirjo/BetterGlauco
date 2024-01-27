from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import redirect
import django_tables2 as tables2
from django.views.generic import FormView, TemplateView, UpdateView

from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares
from .filtros import FiltroPosicaoData
from .forms import FormPosicaoData
from .tabelas import TabelaPosicaoAtivos
from investimento.models import AtivoPerfilCaixa, InstituicaoFinanceira, PosicaoData


class InicioAtualizacao(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    

class DividendosInicio(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 
    

class DividendoNovo(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class DividendoEditar(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'


class PosicaoCorretora(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class PosicaoCorretoraNova(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class PosicaoCorretoraEditar(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class PosicaoIndividual(LoginRequiredMixin, tables2.SingleTableMixin, FilterView):
    filterset_class = FiltroPosicaoData
    table_class = TabelaPosicaoAtivos
    template_name = 'posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['titulo_pagina'] = 'Atualizar por ativo'
        context['nome_parametro'] = 'valor atualizado'
        context['url_insert'] = 'invest_atualizacao:posicao_individual_nova'
        return context 
    
    
    def get_filterset(self, *args, **kwargs):
        fs = super().get_filterset(*args, **kwargs)
        fs.filters['ativo_perfil_caixa__corretora'].field.queryset = InstituicaoFinanceira.objects.filter(perfil=self.request.session['id_perfil_selecionado'])
        return fs
    
    
    def get_queryset(self, **kwargs):
        return PosicaoData.objects.filter(
            ativo_perfil_caixa__subclasse__caixa__perfil=Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
            ).order_by('-data')
    

class PosicaoIndividualNova(LoginRequiredMixin, FormView):
    form_class = FormPosicaoData
    template_name = 'atualizar_posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['nome_parametro'] = 'valor atualizado'
        
        context['form'].fields['ativo_perfil_caixa'].queryset = AtivoPerfilCaixa.objects \
            .filter(subclasse__caixa__perfil=context['id_perfil_selecionado']) \
            .order_by('subclasse__caixa__nome','ativo__ticket','ativo__nome')
        
        return context 
    
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        operacao = form.save(commit=False)
        operacao.save() 
        messages.success(self.request, 'Posição do ativo incluída com sucesso')
        return redirect('invest_atualizacao:posicao_individual')   
    
    
class PosicaoIndividualEditar(LoginRequiredMixin, UpdateView):
    form_class = FormPosicaoData
    model = PosicaoData
    template_name = 'atualizar_posicao_ativo.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['nome_parametro'] = 'valor atualizado'
        
        context['form'].fields['ativo_perfil_caixa'].queryset = AtivoPerfilCaixa.objects \
            .filter(subclasse__caixa__perfil=context['id_perfil_selecionado']) \
            .order_by('subclasse__caixa__nome','ativo__ticket','ativo__nome')
        
        return context 
    
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        operacao = form.save(commit=False)
        operacao.save() 
        messages.success(self.request, 'Posição do ativo atualizada com sucesso')
        return redirect('invest_atualizacao:posicao_individual')  
    