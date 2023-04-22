import django_tables2 as tables


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