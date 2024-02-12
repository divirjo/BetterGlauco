from django import forms
from investimento.models import PosicaoDataFundo

class FormPosicaoDataFundo(forms.ModelForm):
    
    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'