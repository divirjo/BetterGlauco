from investimento.models import Parametro

class Constante():
    
    def BDR_CUSTO(self):
        objeto = Parametro.objects.get_or_create(nome='BDR_CUSTO',
                                                defaults={'valor': '1.0038',
                                                          'descricao': 'Estimativa de custos operacionais para criar o BDR'})
        return float(objeto[0].valor)
    
    def BDR_IMPOSTO_DIVIDENDOS_USA(self):
        objeto = Parametro.objects.get_or_create(nome='BDR_IMPOSTO_DIVIDENDOS_USA',
                                                defaults={'valor': '0.441826',
                                                          'descricao': 'fator para cálculo do imposto de renda sobre dividendos retido nos EUA para os BDRs'})
        return float(objeto[0].valor)
    
    def E_MAIL_API_SCRAPERLINK(self):
        objeto = Parametro.objects.get_or_create(nome='E_MAIL_API_SCRAPERLINK',
                                                defaults={'valor': '',
                                                          'descricao': 'E-mail cadastrado na API scraperlink.com/investpy'})
        return  objeto[0].valor
    
    