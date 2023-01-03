from django.contrib import messages
from django.utils import timezone
import requests
from .models import Ativo

class BRD():
    
    def __init__(self, request):
        self.dolar_venda = 0.0
        self.dolar_compra = 0.0
        self._request = request
        
        if self._request.GET.get('ticket'):
            self.ativo_selecionado = self.carregaAtivo(self._request.GET.get('ticket'))
            self.get_cotacao_dolar()
        else:
            messages.warning(self._request, 'Ativo não informado')
            self.ativo_selecionado = Ativo()
        
    def carregaAtivo(self, ticker_informado):
        ativos_localizados = Ativo.objects.filter(ticket__icontains=ticker_informado)
        
        if len(ativos_localizados) > 0:
            return ativos_localizados[0]
        else:
            messages.error(self._request, 'Ativo {} não cadastrado'.format(ticker_informado))
            return Ativo()
    
    def get_cotacao_dolar(self):
        '''
        Obtem o valor do dolar para venda e compra, consultando a API do Banco Central
        '''
        data_atual = timezone.now().strftime(f"%m-%d-%Y")
        link_api_bacen = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaAberturaOuIntermediario(codigoMoeda=@codigoMoeda,dataCotacao=@dataCotacao)?@codigoMoeda='USD'&@dataCotacao='{}'&$format=json".format(data_atual)
        dados = requests.get(link_api_bacen)
        dados_dic = dados.json()
        
        if len(dados_dic['value']) < 1:
            messages.error(self._request, 'Cotação dolar indisponível: ')
            return
        
        self.dolar_venda = dados_dic['value'][0]['cotacaoCompra']
        self.dolar_compra = dados_dic['value'][0]['cotacaoVenda']
        
