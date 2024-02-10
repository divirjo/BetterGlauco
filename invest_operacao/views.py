from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django_filters.views import FilterView
import django_tables2 as tables2 
from django_tables2.paginators import LazyPaginator
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView

from .filtros_operacoes import FiltroOperacaoAtivo
from .forms_operacoes import FormOperacaoNotaCorretagem, \
                                FormExtratoOperacao
from .nota_corretagem import registrar_nota_corretagem
from .tabelas import TabelaExtratoOperacoes, tabelaNotaCorretagem
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
        fs.filters['ativo_perfil_caixa'].field.queryset = \
            fs.filters['ativo_perfil_caixa'].field.queryset.filter(
                    subclasse__caixa__perfil_id= \
                        self.request.session['id_perfil_selecionado']
            )
        fs.filters['ativo_perfil_caixa'].field.order_by = (
            'ativo_perfil_caixa__ativo__ticket',
            'ativo_perfil_caixa__ativo__nome'
        )
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
    
    
class RegistraNotaCorretagem(LoginRequiredMixin, FormView):
    form_class = FormOperacaoNotaCorretagem
    template_name = 'registrar_nota_corretagem.html'
    nota = registrar_nota_corretagem() 
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        context['titulo_pagina'] = 'Registrar nota de corretagem'
        context['nome_botao_form'] = 'Incluir ativo'
        
        context['form'].fields['ativoPerfilCaixa'].choices = AtivoPerfilCaixa.objects \
            .annotate(ativo_com_ticket=Concat('ativo__ticket', Value(' : '), 'ativo__nome')) \
            .filter(subclasse__caixa__perfil__pk=
                    context['id_perfil_selecionado']) \
            .values_list('pk','ativo_com_ticket') \
            .order_by('ativo_com_ticket')
        
        if(self.request.GET.get('atualizar_nota')):
            self.atualiza_nota_corretagem()
        
        if(self.request.GET.get('incluirAtivo')):
            self.incluir_ativo_nota()
        
        if not self.kwargs.get('id_linha') is None:
            self.nota.id_linha_selecionada = int(self.kwargs.get('id_linha'))
            context = self.carrega_dados_linha(context)
        
        if(self.request.GET.get('salvar')):
            retorno = self.nota.salvar_operacoes_nota()
            messages.success(self.request, retorno)
            
        if(self.request.GET.get('novaNota')):
            self.nota.nova_nota_corretagem()
         
        context['data'] = self.nota._data
        context['total_custos'] = str(self.nota._total_custos)
        context['ir_fonte'] = str(self.nota._ir_fonte)
        
        context['table'] =  tabelaNotaCorretagem(self.nota.get_dict_nota_corretagem())
        
        return context 
    
       
    def incluir_ativo_nota(self):
        """
        Função para incluir ou atualizar um ativo na nota de corretagem
        
        Returns:
            None
        """
        
        ativo_perfil_caixa_id = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('ativoPerfilCaixa'))
        operacao = self.request.GET.get('operacao')
        quantidade = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('quantidade'))
        valor_unitario = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('valor_unitario'))

        if self.nota.id_linha_selecionada != -1:
            self.nota.alterar_ativo_nota(ativo_perfil_caixa_id, operacao, quantidade, valor_unitario)
            self.nota.id_linha_selecionada = -1
        else:
            self.nota.incluir_ativo_nota(ativo_perfil_caixa_id, operacao, quantidade, valor_unitario)
        


    def carrega_dados_linha(self, context):
        linha = self.nota.get_dict_nota_corretagem()[self.nota.id_linha_selecionada]
        context['form'].fields['ativoPerfilCaixa'].initial =linha['ativo_perfil_caixa_id']
        context['form'].fields['operacao'].initial = linha['operacao']
        context['form'].fields['quantidade'].initial = linha['quantidade']
        context['form'].fields['valor_unitario'].initial = linha['valor_unitario']
        context['nome_botao_form'] = 'Atualizar ativo'
        
        return context

        
    def atualiza_nota_corretagem(self):
        
        if len(self.request.GET.get('data')) > 0:
            data = datetime.strptime(self.request.GET.get('data'), r'%Y-%m-%d')
            if data != self.nota._data:
                self.nota.set_data_nota(data)
                
        if len(self.request.GET.get('total_custos')) > 0:
            total_custos = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('total_custos'))
            self.nota.set_total_custos(total_custos)

        if len(self.request.GET.get('ir_fonte')) > 0:
            ir_fonte = Funcoes_auxiliares.converte_numero_str(self.request.GET.get('ir_fonte'))
            self.nota.set_ir_fonte(ir_fonte)
            
    
        
        
