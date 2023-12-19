from typing import Any
from django import forms
from investimento.models import Ativo, Caixa, ClasseAtivo, InstituicaoFinanceira
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class FormAtivo(forms.ModelForm):
    
    class Meta:
        model = Ativo
        fields = '__all__'
        widgets = {
            'desdobramento': forms.NumberInput(attrs={'step': 1}),
        }


class FormCaixa(forms.ModelForm):
    
    class Meta:
        model = Caixa
        fields = '__all__'
        exclude = ('perfil',)
        
        
class FormClasseAtivo(forms.ModelForm):
    
    class Meta:
        model = ClasseAtivo
        fields = '__all__'
        exclude = ('perfil',)      
    
class FormInstituicaoFinanceira(forms.ModelForm):
    
    class Meta:
        model = InstituicaoFinanceira
        fields = '__all__'
        exclude = ('perfil',)
        
