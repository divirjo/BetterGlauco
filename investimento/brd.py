from django.contrib import messages
from django.utils import timezone
import requests
from .models import Ativo
from BetterGlauco.parametro import Constante


class BRD():
    _CONSTANTE = Constante()
    
    def __init__(self, request, ticket):
        self.dolar_venda = 0.0
        self.dolar_compra = 0.0
        self.ticket_original_valor_us = 0.0
        self.preco_referencia_compra = 0.0
        self.preco_referencia_venda = 0.0
        self.custos_brd = self._CONSTANTE.BRD_CUSTO()
        self._request = request
        
        if ticket:
            self.ativo_selecionado = self.carregaAtivo(ticket)
        else:
            messages.warning(self._request, 'Ativo não informado')
            self.ativo_selecionado = Ativo()
        
    def carregaAtivo(self, ticker_informado):
        ativos_localizados = Ativo.objects.filter(ticket__icontains=ticker_informado)
        
        if len(ativos_localizados) > 0:
            # Neste caso, qualquer ativo é aceito, pois os dados utilizados no cálculo não tem relação com o perfil ativo
            return ativos_localizados[0]
        else:
            messages.error(self._request, 'Ativo {} não cadastrado'.format(ticker_informado))
            return Ativo()

    def calcular_preco_referencia(self, valor_US):
        if self.ativo_selecionado.ticket:
            self.get_cotacao_dolar()
            if valor_US > 0:
                self.ticket_original_valor_us = valor_US
            else:
                self.get_cotacao_ticker_referencia()
            self.get_preco_referencia()

    
    def get_cotacao_dolar(self):
        '''
        Obtém o valor do dolar para venda e compra, consultando a API do Banco Central
        '''
        data_atual = timezone.now().strftime(f"%m-%d-%Y")
        link_api_bacen = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaAberturaOuIntermediario(codigoMoeda=@codigoMoeda,dataCotacao=@dataCotacao)?@codigoMoeda='USD'&@dataCotacao='{}'&$format=json".format(data_atual)
        dados = requests.get(link_api_bacen)
        dados_dic = dados.json()
        
        if len(dados_dic['value']) < 1:
            messages.error(self._request, 'Cotação dolar indisponível.')
            return
        
        self.dolar_venda = dados_dic['value'][0]['cotacaoCompra']
        self.dolar_compra = dados_dic['value'][0]['cotacaoVenda']
        
    def get_cotacao_ticker_referencia(self):
        '''
        Obtém o valor do ticker de referência, em dólar
        '''
              
        data_atual = timezone.now().strftime(f"%Y-%m-%d")
             
        self.ticket_original_valor_us = self.consultar_api_cotacoes(data_atual)
        if self.ticket_original_valor_us == 0.0:
            messages.info(self._request, 'Cotação internacional do ativo indisponível. Exibindo dados de ontem')
            data_anterior = (timezone.now() - timezone.timedelta(days=1)).strftime(f"%Y-%m-%d")
            self.ticket_original_valor_us = self.consultar_api_cotacoes(data_anterior)
        
    
    def consultar_api_cotacoes(self, data_consulta):
        e_mail = self._CONSTANTE.E_MAIL_API_SCRAPERLINK()
        link_api='http://api.scraperlink.com/investpy/?email={}&type=historical_data&product=etfs&from_date={}&to_date={}&time_frame=Daily&country=united%20states&symbol={}'.format(e_mail, data_consulta, data_consulta, self.ativo_selecionado.ticket_original)
        print (link_api)
        dados = requests.get(link_api)
        dados_dic = dados.json()
        
        if  dados_dic['data']:
            return dados_dic['data'][0]['last_close']
        else:
            return 0.0
        
    
    def get_preco_referencia(self):
        self.preco_referencia_compra = float(self.dolar_venda) * float(self.ticket_original_valor_us) * float(self.custos_brd)  / float(self.ativo_selecionado.desdobramento)
        self.preco_referencia_venda = float(self.dolar_compra) * float(self.ticket_original_valor_us) * float(self.custos_brd) / float(self.ativo_selecionado.desdobramento)