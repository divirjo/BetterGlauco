from django import forms
from django_filters import FilterSet, ModelChoiceFilter

from investimento.models import Ativo, AtivoPerfilCaixa, InstituicaoFinanceira, PosicaoData 

'''
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.corretora

class CustomModelChoiceFilter(ModelChoiceFilter):
    field_class = CustomModelChoiceField
'''

class FiltroAtivoFundos(FilterSet):
    
    ativo_perfil_caixa = ModelChoiceFilter(
        field_name = 'ativo_perfil_caixa',
        queryset=Ativo.objects.filter(
            cota_bolsa=False
            ),
        label='Selecione o ativo', 
    )

    class Meta:
        model = PosicaoData
        fields = {'ativo_perfil_caixa': ['exact']}  


class FiltroCorretoraAtivo(FilterSet):
    
    ativo_perfil_caixa__corretora = ModelChoiceFilter(
        field_name = 'ativo_perfil_caixa__corretora',
        queryset=InstituicaoFinanceira.objects.all(),
        label='Selecione a corretora', 
    )

    class Meta:
        model = PosicaoData
        fields = {'ativo_perfil_caixa__corretora': ['exact']}  