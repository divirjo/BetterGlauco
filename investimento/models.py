from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone

LISTA_OPERACOES = (
    ('VENDA', 'Venda'),
    ('COMPRA', 'Compra')
)


class Parametro(models.Model):
    """
    Model com as parametrizações do sistema
    """
    BRD_CUSTO = models.DecimalField(max_digits=8,
                                decimal_places=4,
                                default=1.0038)
    E_MAIL_API = models.EmailField(default='')



class Usuario(AbstractUser):
    observacao = models.TextField(max_length=1000)


class Perfil(models.Model):
    usuarios_permitidos = models.ManyToManyField('Usuario')   
    nome = models.TextField(max_length=25)
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class Caixa(models.Model):
    perfil = models.ForeignKey('Perfil', 
                               related_name='caixas',
                               on_delete=models.DO_NOTHING)
    nome = models.TextField(max_length=100)
    cota_sistema_valor = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    alocacao_teorica_valor = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    alocacao_teorica_percentual = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.perfil.nome + ' - ' + self.nome    



class InstituicaoFinanceira(models.Model):
    nome = models.TextField(max_length=100)
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome   


class Ativo(models.Model):
    alocacao_caixa = models.ForeignKey('Caixa', 
                                       related_name='ativos',
                                       on_delete=models.DO_NOTHING)
    corretora = models.ForeignKey('InstituicaoFinanceira', 
                                  related_name='ativos',
                                  on_delete=models.DO_NOTHING)
    # Código da bolsa do ativo ou um apelido do fundo
    ticket = models.TextField(max_length=10)
    nome = models.TextField(max_length=100)
    cnpj = models.TextField(max_length=19)
    # Parametrização BRDS (ativo referência e desdobramento)
    ticket_original = models.TextField(max_length=10)
    desdobramento = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0)
    # Percentual ideal de alocao do ativo
    alocacao_teorica_valor = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    alocacao_teorica_percentual = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return (self.alocacao_caixa.perfil.nome + ' - ' + 
                self.ticket + ': ' + 
                self.nome)   
    

class PosicaoData(models.Model):
    """
    Nesta tabela são armazenados as atualizações de valor dos investimentos, viabilizando a análise histórica.
    """
    ativo = models.ForeignKey('Ativo', 
                              related_name='posicoes',
                              on_delete=models.PROTECT)
    data = models.DateTimeField(default=timezone.now)
    # cotas do ativo, disponibilizada na corretora
    cota_ativo_quantidade = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0)
    # quantidade de cotas calculadas pelo sistema
    cota_sistema_quantidade = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0)
    # valor cota do sistema
    cota_sistema_valor = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    # valor dividendos recebibos
    dividendos = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return (self.ativo.alocacao_caixa.perfil.nome + ' - ' + 
                self.ativo.ticket + ': ' + 
                self.data.strftime(f"%Y-%m-%d"))  

    
class ExtratoOperacao(models.Model):
    """
    Model da tabela que discrimina as operações de compra e venda de ativos
    """
    ativo = models.ForeignKey('Ativo', 
                                  related_name='operacoes',
                                  on_delete=models.PROTECT)
    data = models.DateTimeField(default=timezone.now)
    operacao = models.CharField(max_length=10, choices=LISTA_OPERACOES)
    valor_unitario = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    custos_transacao = MoneyField(max_digits=19, 
                       decimal_places=4, 
                       default_currency='BRL',
                       default=0)
    quantidade = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0)
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return (self.ativo.alocacao_caixa.perfil.nome + ' - ' + 
                self.ativo.ticket + ': ' + 
                self.data.strftime(f"%Y-%m-%d"))    