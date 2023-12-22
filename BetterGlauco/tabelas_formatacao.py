import django_tables2 as tables
from django.utils.html import format_html
import locale



class ColunaNumericaDecimal(tables.Column):
    def render(self, value, column):
        if value < 0:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-red-800 text-right"
                                }
                            }
        else:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 text-right"
                                }
                            }
            
        return '{:0.2f}'.format(value)
    
    
class ColunaSomaNumericaDecimal(tables.Column):
    def render(self, value, column):
        if value < 0:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-red-800 text-right"
                                },
                            "tf":{
                                "class":"px-6 py-4 text-right"
                                }
                            }
        else:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 text-right"
                                },
                            "tf":{
                                "class":"px-6 py-4 text-right"
                                }
                            }
            
        return '{:0.2f}'.format(value)
    
    def render_footer(self, bound_column, table):
        return '{:0.2f}'.format(sum(bound_column.accessor.resolve(linha) 
                    for linha in table.data))
 
    
class ColunaDinheiro(tables.Column):
    def render(self, value, column):
        
        if value < 0:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-red-800 text-right"
                                }
                            }
        else:
            column.attrs = {"td":{
                                "class":"px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 text-right"
                                }
                            }
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')    
        return locale.currency(value, grouping=True, symbol=None)