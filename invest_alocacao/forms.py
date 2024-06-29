
from django import forms

from investimento.models import (
    Ativo,
    AtivoPerfilCaixa,
    Caixa,
    ClasseAtivo,
    InstituicaoFinanceira,
)


class FormAtivo(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = '__all__'
        widgets = {
            'desdobramento': forms.NumberInput(attrs={'step': 1}),
        }


class FormAtivoPerfilCaixa(forms.ModelForm):
    class Meta:
        model = AtivoPerfilCaixa
        fields = '__all__'
        exclude = ('perfil',)


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
