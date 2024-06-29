from django_filters import CharFilter, FilterSet, ModelChoiceFilter

from investimento.models import Ativo, Caixa, ClasseAtivo

"""
Documentação: https://django-filter.readthedocs.io/en/stable/ref/filterset.html
"""


class FiltroAtivo(FilterSet):
    ticket = CharFilter(field_name='ticket', lookup_expr='icontains')
    nome = CharFilter(field_name='nome', lookup_expr='icontains')

    class Meta:
        model = Ativo
        fields = {'ticket', 'nome'}


class FiltroClasseAtivo(FilterSet):
    caixa = ModelChoiceFilter(
        queryset=Caixa.objects.all(), label='Selecione uma caixa'
    )

    class Meta:
        model = ClasseAtivo
        fields = {'caixa': ['exact']}
        # fields = {'nome': ['exact', 'contains'], 'caixa': ['exact']}
