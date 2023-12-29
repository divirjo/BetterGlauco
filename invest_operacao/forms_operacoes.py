from typing import Any
from django import forms
from investimento.models import ExtratoOperacao

class FormExtratoOperacao(forms.ModelForm):
    
    class Meta:
        model = ExtratoOperacao
        fields = '__all__'