import django_tables2 as tables

'''
Informações:
https://enzircle.com/responsive-table-with-django-and-htmx

https://github.com/jieter/django-tables2

https://django-tables2.readthedocs.io/

'''

class Tabela_brd_dividendos_impostos(tables.Table):
    valor_dividendo = tables.Column()
    valor_dividendo.verbose_name = 'Dividendos recebidos (R$)'
    
    valor_impostos = tables.Column()
    valor_impostos.verbose_name = 'Impostos USA estimados (R$)'
    
    class Meta:
        template_name = 'tables/semantic.html'
       
    
    
