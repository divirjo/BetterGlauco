from typing import Any
from django import forms
from .models import Ativo, InstituicaoFinanceira
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class FormAtivo(forms.ModelForm):
    
    class Meta:
        model = Ativo
        fields = '__all__'
        widgets = {
            'desdobramento': forms.NumberInput(attrs={'step': 1}),
        }

        
class FormInstituicaoFinanceira(forms.ModelForm):
    
    class Meta:
        model = InstituicaoFinanceira
        fields = '__all__'
        exclude = ('perfil',)
        
