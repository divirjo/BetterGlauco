from investimento.models import Parametro

class Constante():
    
    def BRD_CUSTO(self):
        objeto = Parametro.objects.get_or_create(nome='BRD_CUSTO',
                                                defaults={'valor': '1.0038',
                                                          'descricao': 'Estimativa de custos operacionais para criar o BRD'})
        return float(objeto[0].valor)
    
    def BRD_IMPOSTO_DIVIDENDOS_USA(self):
        objeto = Parametro.objects.get_or_create(nome='BRD_IMPOSTO_DIVIDENDOS_USA',
                                                defaults={'valor': '0.441826',
                                                          'descricao': 'fator para cálculo do imposto de renda sobre dividendos retido nos EUA para os BRDs'})
        return float(objeto[0].valor)
    
    def E_MAIL_API_SCRAPERLINK(self):
        objeto = Parametro.objects.get_or_create(nome='E_MAIL_API_SCRAPERLINK',
                                                defaults={'valor': '',
                                                          'descricao': 'E-mail cadastrado na API scraperlink.com/investpy'})
        return  objeto[0].valor
    
    