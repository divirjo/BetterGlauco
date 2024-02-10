from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import redirect
from django_tables2 import MultiTableMixin, SingleTableMixin
from django.views.generic import FormView, TemplateView, UpdateView

from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares
from .filtros import FiltroAtivoFundos, FiltroCorretoraAtivo
from .forms import FormPosicaoData
from .tabelas import TabelaEdicaoPosicaoFundos, TabelaPosicaoFundos, \
    TabelaPosicaoBolsa
from investimento.models import AtivoPerfilCaixa, \
    InstituicaoFinanceira, PosicaoData, PosicaoDataBolsa


class InicioAtualizacao(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        
        query_pos_fundos =  PosicaoData.objects.filter(
                    ativo_perfil_caixa__subclasse__caixa__perfil=id_perfil
                ).order_by('-data')
        tabela_posicao_fundos = TabelaPosicaoFundos(query_pos_fundos)
        context['tabela_posicao_fundos'] = tabela_posicao_fundos
        
        query_pos_bolsa =  PosicaoDataBolsa.objects.all()
        tabela_posicao_bolsa = query_pos_bolsa
        context['tabela_posicao_bolsa'] = tabela_posicao_bolsa
        
        return context 
    

class DividendosInicio(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        return context 
    

class DividendoNovo(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class DividendoEditar(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    


class PosicaoCorretora(LoginRequiredMixin, TemplateView):
    filterset_class = FiltroCorretoraAtivo
    table_class = TabelaEdicaoPosicaoFundos
    template_name = 'posicao_ativo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['titulo_pagina'] = 'Atualizar por ativo'
        context['nome_parametro'] = 'valor atualizado'
        context['url_insert'] = 'invest_atualizacao:posicao_individual_nova'
        return context 
    
    
    def get_filterset(self, *args, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        fs = super().get_filterset(*args, **kwargs)
        fs.filters['ativo_perfil_caixa__corretora'].field.queryset = \
            InstituicaoFinanceira.objects.filter(perfil=id_perfil)
        return fs
    
    
    def get_queryset(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        query = PosicaoData.objects.filter(
                    ativo_perfil_caixa__subclasse__caixa__perfil=id_perfil
                ).order_by('-data')
        return query
    

class PosicaoCorretoraNova(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class PosicaoCorretoraEditar(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class PosicaoIndividual(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = FiltroAtivoFundos
    table_class = TabelaEdicaoPosicaoFundos
    template_name = 'posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['titulo_pagina'] = 'Atualizar por ativo (fundos)'
        context['nome_parametro'] = 'valor atualizado'
        context['url_insert'] = 'invest_atualizacao:posicao_individual_nova'
        return context 
    
    
    def get_filterset(self, *args, **kwargs):
        fs = super().get_filterset(*args, **kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        fs.filters['ativo_perfil_caixa'].field.queryset = \
            AtivoPerfilCaixa.objects.filter(
                subclasse__caixa__perfil=id_perfil,
                ativo__cota_bolsa=False
            )
        return fs
    
    
    def get_queryset(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        query = PosicaoData.objects.filter(
            ativo_perfil_caixa__subclasse__caixa__perfil= id_perfil
            ).order_by('-data')
        return query
    

class PosicaoIndividualNova(LoginRequiredMixin, FormView):
    form_class = FormPosicaoData
    template_name = 'atualizar_posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'
        
        query = AtivoPerfilCaixa.objects.filter(
                subclasse__caixa__perfil=context['id_perfil_selecionado'],
                ativo__cota_bolsa=False
            ).order_by(
                'subclasse__caixa__nome',
                'ativo__ticket',
                'ativo__nome'
            )
        context['form'].fields['ativo_perfil_caixa'].queryset = query
            
        return context 
    
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
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
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'
        
        query = AtivoPerfilCaixa.objects.filter(
                subclasse__caixa__perfil=context['id_perfil_selecionado']
            ).order_by(
                'subclasse__caixa__nome',
                'ativo__ticket',
                'ativo__nome'
            )
        context['form'].fields['ativo_perfil_caixa'].queryset = query
            
        return context 
    
    
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        operacao = form.save(commit=False)
        operacao.save()
        mensagem = 'Posição do ativo atualizada com sucesso' 
        messages.success(self.request, mensagem)
        return redirect('invest_atualizacao:posicao_individual')  
    