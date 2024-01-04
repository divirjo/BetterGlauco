from django import forms
from typing import Any
from investimento.models import ExtratoOperacao, \
                                LISTA_OPERACOES, \
                                AtivoPerfilCaixa


class FormOperacaoNotaCorretagem(forms.Form):

    id_linha = forms.IntegerField()
    
    ativoPerfilCaixa = forms.ChoiceField(label='Ativo')
    
    operacao = forms.ChoiceField(choices=LISTA_OPERACOES,
                                 initial='COMPRA',
                                 label='Operação')
    
    quantidade = forms.DecimalField(label='Quantidade')
    
    valor_unitario = forms.DecimalField(label='Valor Unitário')


class FormExtratoOperacao(forms.ModelForm):
    
    class Meta:
        model = ExtratoOperacao
        fields = '__all__'
        
        