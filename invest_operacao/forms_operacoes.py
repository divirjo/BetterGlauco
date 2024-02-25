from django import forms
from investimento.models import ExtratoOperacao, TipoOperacao


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


class FormExtratoOperacaoBolsa(forms.ModelForm):
    
    class Meta:
        model = ExtratoOperacao
        fields = '__all__'

        
class FormExtratoOperacaoFundo(forms.ModelForm):
    
    
    valor_total = forms.DecimalField(
        label='Valor Total',
        help_text='Ao preencher o valor total, o sistema calculará automaticamente a quantidade de cotas',
    )
    
    class Meta:
        model = ExtratoOperacao
        fields = '__all__'
        exclude = ('quantidade','valor_unitario')
