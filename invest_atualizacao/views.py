from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import redirect
from django_tables2 import SingleTableMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares
from .cotas_ativo import CotaAtivo
from .filtros import FiltroAtivoBolsa, FiltrosCombinadosCorretora
from .forms import FormPosicaoDataBolsa, FormEditarPosicaoDataFundo, \
    FormNovaPosicaoDataFundo
from .tabelas import TabelaPosicaoBolsa, TabelaPosicaoFundos
    
from investimento.models import Ativo, AtivoPerfilCaixa, \
    InstituicaoFinanceira, PosicaoDataFundo, PosicaoDataBolsa


class InicioAtualizacao(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'   
    
    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)

        query_pos_fundos =  PosicaoDataFundo.objects.filter(
                    ativo_perfil_caixa__subclasse__caixa__perfil=id_perfil
                ).order_by('-data')
        tabela_posicao_fundos = TabelaPosicaoFundos(query_pos_fundos)
    
        query_pos_bolsa =  PosicaoDataBolsa.objects.all()
        tabela_pos_bolsa = TabelaPosicaoBolsa(query_pos_bolsa)
        
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['tabela_posicao_fundos'] = tabela_posicao_fundos
        context['tabela_posicao_bolsa'] = tabela_pos_bolsa   
        return context 
    

class DividendosInicio(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        return context 
    

class DividendoNovo(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    

class DividendoEditar(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'  


class PosicaoIndividualBolsa(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = FiltroAtivoBolsa
    table_class = TabelaPosicaoBolsa
    template_name = 'posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['titulo_pagina'] = 'Atualizar por ativo (bolsa)'
        context['nome_parametro'] = 'valor atualizado'
        context['url_insert'] = \
            'invest_atualizacao:posicao_individual_bolsa_nova'
        messages.warning(
            self.request, 
            'Cadastro geral. Alterações aqui afetarão todos os usuários do sistema'
        )
        return context 
    
    
    def get_queryset(self, **kwargs):
        query = PosicaoDataBolsa.objects.all().order_by('-data')
        return query
    

class PosicaoIndividualBolsaNova(LoginRequiredMixin, FormView):
    form_class = FormPosicaoDataBolsa
    template_name = 'atualizar_posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        
        query_ativos = Ativo.objects.filter(cota_bolsa=True) \
            .order_by('ticket','nome')
        
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'  
        context['url_retorno'] = \
            'invest_atualizacao:posicao_individual_bolsa'  
        context['form'].fields['ativo'].queryset = query_ativos
        return context 
    
    
    def form_valid(self, form, **kwargs):
        operacao = form.save(commit=False)
        operacao.save() 
        mensagem = 'Posição do ativo {} incluída com sucesso' \
            .format(operacao.ativo.ticket) 
        return redirect('invest_atualizacao:posicao_individual_bolsa')   
    
    
class PosicaoIndividualBolsaEditar(LoginRequiredMixin, UpdateView):
    form_class = FormPosicaoDataBolsa
    model = PosicaoDataBolsa
    template_name = 'atualizar_posicao_ativo.html'
    

    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        
        query_ativos = Ativo.objects.filter(cota_bolsa=True) \
            .order_by('ticket','nome')
        
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'
        context['url_retorno'] = \
            'invest_atualizacao:posicao_individual_bolsa'
        context['form'].fields['ativo'].queryset = query_ativos
        return context 
    
    
    def form_valid(self, form, **kwargs):
        operacao = form.save(commit=False)
        operacao.save()
        mensagem = 'Posição do ativo {} atualizada com sucesso' \
            .format(operacao.ativo.ticket) 
        messages.success(self.request, mensagem)
        return redirect('invest_atualizacao:posicao_individual_bolsa') 


class PosicaoIndividualFundo(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = FiltrosCombinadosCorretora
    table_class = TabelaPosicaoFundos
    template_name = 'posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['titulo_pagina'] = 'Atualizar por ativo (fundos)'
        context['nome_parametro'] = 'valor atualizado'
        context['url_insert'] = \
            'invest_atualizacao:posicao_individual_fundo_nova'
        return context 
    
    
    def get_filterset(self, *args, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        fs = super().get_filterset(*args, **kwargs)
        
        fs.filters['ativo_perfil_caixa__corretora'].field.initial = 2
        fs.filters['ativo_perfil_caixa__corretora'].field.label = 'Corretora'
        fs.filters['ativo_perfil_caixa__corretora'].field.queryset = \
            InstituicaoFinanceira.objects.filter(perfil=id_perfil)
        
        corretora_selecionada = Funcoes_auxiliares.converte_numero_str(
            self.request.GET.get('ativo_perfil_caixa__corretora')
        ) 
        if corretora_selecionada > 0:
            fs.filters['ativo_perfil_caixa'].field.queryset = \
                AtivoPerfilCaixa.objects.filter(
                    subclasse__caixa__perfil=id_perfil,
                    ativo__cota_bolsa=False,
                    corretora=corretora_selecionada
            )
        else:
            fs.filters['ativo_perfil_caixa'].field.queryset = \
                AtivoPerfilCaixa.objects.filter(
                    subclasse__caixa__perfil=id_perfil,
                    ativo__cota_bolsa=False
            )
            
        return fs
    
    
    def get_queryset(self, **kwargs):
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        query = PosicaoDataFundo.objects.filter(
            ativo_perfil_caixa__subclasse__caixa__perfil= id_perfil
            ).order_by('-data')
        return query
    

class PosicaoIndividualFundoNova(LoginRequiredMixin, FormView):
    form_class = FormNovaPosicaoDataFundo
    template_name = 'atualizar_posicao_ativo.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'  
        context['url_retorno'] = \
            'invest_atualizacao:posicao_individual_fundo'
                 
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
        valor_total = form.cleaned_data['valor_total']
        valor_total_dolar = form.cleaned_data['valor_total_dolar']
        
        operacao = form.save(commit=False)
        
        cotas_ativo = CotaAtivo(operacao.ativo_perfil_caixa.ativo.id)        
        total_cotas = cotas_ativo.quantidadeTotal()
        operacao.cota_sistema_valor = valor_total / total_cotas
        operacao.cota_valor_dolar = valor_total_dolar / total_cotas
        operacao.save() 
        
        mensagem =  'Posição do ativo {} incluída com sucesso' \
            .format(operacao.ativo_perfil_caixa.ativo.nome)
        messages.success(self.request, mensagem)
        return redirect('invest_atualizacao:posicao_individual_fundo_nova')   
    
    
class PosicaoIndividualFundoEditar(LoginRequiredMixin, UpdateView):
    form_class = FormEditarPosicaoDataFundo
    model = PosicaoDataFundo
    template_name = 'atualizar_posicao_ativo.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_perfil = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['id_perfil_selecionado'] = id_perfil 
        context['nome_parametro'] = 'valor atualizado'
        context['url_retorno'] = \
            'invest_atualizacao:posicao_individual_fundo'
        
        query_ativos = AtivoPerfilCaixa.objects \
            .filter(
                subclasse__caixa__perfil=context['id_perfil_selecionado']
            ).order_by(
                'subclasse__caixa__nome',
                'ativo__ticket',
                'ativo__nome'
            )
        context['form'].fields['ativo_perfil_caixa'].queryset = query_ativos
            
        return context 
    
    
    def form_valid(self, form, **kwargs):
        operacao = form.save(commit=False)
        operacao.save()
        mensagem = 'Posição do ativo atualizada com sucesso' 
        messages.success(self.request, mensagem)
        return redirect('invest_atualizacao:posicao_individual_fundo')  
    

 
    