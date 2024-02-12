from django import forms
from typing import Any
from investimento.models import ExtratoOperacao, \
    TipoOperacao


class FormOperacaoNotaCorretagem(forms.Form):

    id_linha = forms.IntegerField()
    
    ativoPerfilCaixa = forms.ChoiceField(label='Ativo')
    
    operacao = forms.ChoiceField(
        choices=TipoOperacao.choices,
        initial=TipoOperacao.COMPRA,
        label='Operação'
    )
    
    quantidade = forms.DecimalField(label='Quantidade')
    
    valor_unitario = forms.DecimalField(label='Valor Unitário')


class FormExtratoOperacao(forms.ModelForm):
    
    class Meta:
        model = ExtratoOperacao
        fields = '__all__'
        
        