import django_tables2 as tables
from django.utils.html import format_html
import locale

class ParametrosTabelas():
    
    CSS_PADRAO = {
        'table':{
            'class':'min-w-full'
        },
        'thead':{
            'class':'bg-amber-900 border-b'
        },
        'th':{
            'class':'text-sm font-medium text-white px-6 py-4 text-left'
        },
        'td':{
            'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                text-gray-900'
        },
        'tfoot':{
            'class':'text-sm font-bold text-gray-900 px-6 py-4' 
        },
    }

    CSS_LINK = {
        'td':{
            'class':'text-center text-dark font-medium text-base py-3 px-2' 
        },
        'a':{
            'class':'border border-amber-900 rounded-md py-1 px-4 \
                text-amber-900 inline-block rounded hover:bg-amber-900 \
                hover:text-white' 
        },
    }
    

class ColunaData(tables.Column):
    def render(self, value, column):
        return value.strftime(r'%d/%m/%Y')


class ColunaNumericaDecimal(tables.Column):
    def render(self, value, column):
        if value < 0:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-red-800 text-right'
                }
            }
        else:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-gray-900 text-right'
                }
            }

        return '{:0.2f}'.format(value)
    
    
class ColunaSomaNumericaDecimal(tables.Column):
    def render(self, value, column):
        if value < 0:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-red-800 text-right'
                },
                'tf':{
                    'class':'px-6 py-4 text-right'
                }
            }
        else:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-gray-900 text-right'
                },
                'tf':{
                    'class':'px-6 py-4 text-right'
                }
            }
            
        return '{:0.2f}'.format(value)
    
    def render_footer(self, bound_column, table):
        return '{:0.2f}'.format(sum(bound_column.accessor.resolve(linha) 
                    for linha in table.data))
 
    
class ColunaDinheiro(tables.Column):
    def render(self, value, column):
        
        if value < 0:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-red-800 text-right'
                }
            }
        else:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-gray-900 text-right'
                }
            }
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')    
        return locale.currency(value, grouping=True, symbol=None)
    
    
class ColunaSomaDinheiro(tables.Column):
    def render(self, value, column):
        if value < 0:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-red-800 text-right'
                },
                'tf':{
                    'class':'px-6 py-4 text-right'
                }
            }
        else:
            column.attrs = {
                'td':{
                    'class':'px-6 py-4 whitespace-nowrap text-sm font-medium \
                        text-gray-900 text-right'
                },
                'tf':{
                    'class':'px-6 py-4 text-right'
                }
            }
            
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')    
        return locale.currency(value, grouping=True, symbol=None)
    
    def render_footer(self, bound_column, table):
        
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')    
        return locale.currency(sum(bound_column.accessor.resolve(linha) 
                    for linha in table.data),grouping=True, symbol=None)