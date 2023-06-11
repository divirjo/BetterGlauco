from django import forms
from .models import Ativo


class FormAtivo(forms.ModelForm):
    
    class Meta:
        model = Ativo
        fields = '__all__'
