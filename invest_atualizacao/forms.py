from django import forms
from investimento.models import PosicaoDataBolsa, PosicaoDataFundo


class FormPosicaoDataBolsa(forms.ModelForm):
    
    class Meta:
        model = PosicaoDataBolsa
        fields = '__all__'
        
        
class FormNovaPosicaoDataFundo(forms.ModelForm):
    
    cota_sistema_valor = forms.DecimalField(
        label='Valor Cota (R$)',
        required=False,
        initial=0,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    cota_valor_dolar = forms.DecimalField(
        label='Valor Cota (US$)',
        initial=0,
        required=False,
    )
    valor_total = forms.DecimalField(label='Valor Total')
    
    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'
        
class FormEditarPosicaoDataFundo(forms.ModelForm):
    
    cota_sistema_valor = forms.DecimalField(
        label='Valor Cota (R$)',
    )
    cota_valor_dolar = forms.DecimalField(
        label='Valor Cota (US$)',
        required=False,
    )
    
    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'