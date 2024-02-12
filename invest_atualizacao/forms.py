from django import forms
from investimento.models import PosicaoDataBolsa, PosicaoDataFundo


class FormPosicaoDataBolsa(forms.ModelForm):
    
    class Meta:
        model = PosicaoDataBolsa
        fields = '__all__'
        
        
class FormPosicaoDataFundo(forms.ModelForm):
    
    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'