from django_filters import FilterSet, ModelChoiceFilter
from investimento.models import Caixa, \
                                ClasseAtivo

'''
Documentação: https://django-filter.readthedocs.io/en/stable/ref/filterset.html
'''


class FiltroClasseAtivo(FilterSet):
    
    caixa = ModelChoiceFilter(
        queryset=Caixa.objects.all(),
        label='Selecione uma caixa' 
    )
    
    class Meta:
        model = ClasseAtivo
        fields = {'caixa': ['exact']}
        #fields = {'nome': ['exact', 'contains'], 'caixa': ['exact']}
        