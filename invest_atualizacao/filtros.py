from django import forms
from django_filters import FilterSet, ModelChoiceFilter

from investimento.models import PosicaoData, AtivoPerfilCaixa, InstituicaoFinanceira

'''
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.corretora

class CustomModelChoiceFilter(ModelChoiceFilter):
    field_class = CustomModelChoiceField
'''

class FiltroPosicaoData(FilterSet):
    
    ativo_perfil_caixa__corretora = ModelChoiceFilter(
        field_name = 'ativo_perfil_caixa__corretora',
        queryset=InstituicaoFinanceira.objects.all(),
        label='Selecione a corretora', 
    )

    class Meta:
        model = PosicaoData
        fields = {'ativo_perfil_caixa__corretora': ['exact']}  