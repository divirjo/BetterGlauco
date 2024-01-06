from django import forms
from investimento.models import PosicaoData

class FormPosicaoData(forms.ModelForm):
    
    class Meta:
        model = PosicaoData
        fields = '__all__'