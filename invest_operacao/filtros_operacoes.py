from django_filters import FilterSet, ModelChoiceFilter

from investimento.models import AtivoPerfilCaixa, ExtratoOperacao


class FiltroOperacaoAtivo(FilterSet):
    ativo_perfil_caixa = ModelChoiceFilter(
        queryset=AtivoPerfilCaixa.objects.all(), label='Selecione um ativo'
    )

    class Meta:
        model = ExtratoOperacao
        fields = {'ativo_perfil_caixa': ['exact']}
