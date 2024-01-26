from django import forms
from django_filters import FilterSet, ModelChoiceFilter

from investimento.models import PosicaoData, AtivoPerfilCaixa

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.corretora

class CustomModelChoiceFilter(ModelChoiceFilter):
    field_class = CustomModelChoiceField

class FiltroPosicaoData(FilterSet):
    
    ativo_perfil_caixa = CustomModelChoiceFilter(
        field_name = 'ativo_perfil_caixa',
        queryset=AtivoPerfilCaixa.objects.all(),
        label='Selecione a corretora', 
    )

    class Meta:
        model = PosicaoData
        fields = {'ativo_perfil_caixa': ['exact']}  