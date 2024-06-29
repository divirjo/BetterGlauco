from django_filters import FilterSet, ModelChoiceFilter

from investimento.models import (
    Ativo,
    InstituicaoFinanceira,
    PosicaoDataBolsa,
    PosicaoDataFundo,
)

"""
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.corretora

class CustomModelChoiceFilter(ModelChoiceFilter):
    field_class = CustomModelChoiceField
"""


class FiltroAtivoBolsa(FilterSet):
    ativo = ModelChoiceFilter(
        field_name='ativo',
        queryset=Ativo.objects.filter(cota_bolsa=True).order_by('ticket'),
        label='Selecione o ativo',
    )

    class Meta:
        model = PosicaoDataBolsa
        fields = {'ativo': ['exact']}


class FiltroAtivoFundos(FilterSet):
    ativo_perfil_caixa = ModelChoiceFilter(
        field_name='ativo_perfil_caixa',
        queryset=Ativo.objects.filter(cota_bolsa=False),
        label='Selecione o ativo',
    )

    class Meta:
        model = PosicaoDataFundo
        fields = {'ativo_perfil_caixa': ['exact']}


class FiltroCorretoraAtivo(FilterSet):
    ativo_perfil_caixa__corretora = ModelChoiceFilter(
        field_name='ativo_perfil_caixa__corretora',
        queryset=InstituicaoFinanceira.objects.all(),
        label='Selecione a corretora',
    )

    class Meta:
        model = PosicaoDataFundo
        fields = {'ativo_perfil_caixa__corretora': ['exact']}


class FiltrosCombinadosCorretora(FilterSet):
    class Meta:
        model = PosicaoDataFundo
        fields = ['ativo_perfil_caixa__corretora', 'ativo_perfil_caixa']
