from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

LISTA_OPERACOES = (
    ('VENDA', 'Venda'),
    ('COMPRA', 'Compra'),
    ('SUBSCRIÇÃO', 'Subscrição'),
    ('DESDOBRO', 'Desdobro')
)


class Parametro(models.Model):
    """
    Model com as parametrizações do sistema
    """
    nome = models.CharField(max_length=100,
                            unique=True,
                            help_text='Nome da constante')
    valor = models.TextField(default='',
                             help_text='Valor da constante')
    descricao = models.TextField(default='',
                             help_text='Descrição da constante')
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome




class Usuario(AbstractUser):
    observacao = models.TextField()


class Perfil(models.Model):
    usuarios_permitidos = models.ManyToManyField('Usuario')   
    nome = models.CharField(max_length=25,
                            help_text='Nome para identificar o perfil (conta de investimento')
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class Ativo(models.Model):
    # Código da bolsa do ativo ou um apelido do fundo
    ticket = models.CharField(max_length=10,
                              default='',
                              blank=True,
                              help_text='Código de negociação do ativo na bolsa')
    nome = models.CharField(max_length=100,
                            help_text='Nome do ativo')
    cnpj = models.CharField(max_length=19,
                            default='',
                            blank=True,
                            help_text='CNPJ do ativo')
    cota_bolsa = models.BooleanField(default=False,
                                     blank=False,
                                    help_text='O ativo possui cota na bolsa?')
    # Parametrização BDRs (ativo referência e desdobramento)
    ticket_original = models.CharField(max_length=10,
                                       default='',
                                       blank=True,
                                       help_text='Código de negociação original do ativo (somente BDRs)')
    desdobramento = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0,
                                help_text='Quanto representa a cota brasileira em relação ao ativo original (somente BDRs)')


    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        
        if self.ticket == '':
            return self.nome
        else:
            return (self.ticket + ': ' + 
                self.nome)   
    

class AtivoPerfilCaixa(models.Model):
    subclasse = models.ForeignKey('ClasseAtivo', 
                                    related_name='ativos_subclasse',
                                    on_delete=models.DO_NOTHING)
    ativo = models.ForeignKey('Ativo', 
                              related_name='posicoes',
                              on_delete=models.PROTECT)
    corretora = models.ForeignKey('InstituicaoFinanceira', 
                                  related_name='ativos',
                                  on_delete=models.DO_NOTHING)
    # Percentual ideal de alocação do ativo
    alocacao_teorica_valor = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    aloc_teor_percent_caixa = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)
    aloc_teor_percent_carteira = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        
        if self.ativo.ticket == '':
            return (self.subclasse.caixa.nome + ' - ' + 
                    self.ativo.nome + ' (' + self.corretora.nome + ')')
        else:
            return (self.subclasse.caixa.nome + ' - ' + 
                self.ativo.ticket + ' - ' + 
                self.ativo.nome + ' (' + self.corretora.nome + ')')     


class Caixa(models.Model):
    perfil = models.ForeignKey('Perfil', 
                               related_name='caixas',
                               on_delete=models.PROTECT)
    nome = models.CharField(max_length=100)
    
    ordem_exibicao = models.IntegerField(default=0)
    
    cota_sistema_valor = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    alocacao_teorica_valor = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    alocacao_teorica_percentual = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome    


class ClasseAtivo(models.Model):
    caixa = models.ForeignKey('Caixa', 
                                related_name='subclasses',
                                on_delete=models.PROTECT)
    nome = models.CharField(max_length=100)
    alocacao_teorica_valor = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    alocacao_teorica_percentual = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.caixa.nome + ' - ' + self.nome    


class InstituicaoFinanceira(models.Model):
    nome = models.TextField(max_length=100)
    perfil = models.ForeignKey('Perfil', 
                              related_name='instituicoes_financeiras',
                              on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome   


class ExtratoOperacao(models.Model):
    """
    Model da tabela que discrimina as operações de compra e venda de ativos
    """
    ativo_perfil_caixa = models.ForeignKey('AtivoPerfilCaixa', 
                              related_name='operacoes',
                              on_delete=models.PROTECT)
    data = models.DateTimeField(default=timezone.now)
    operacao = models.CharField(max_length=10, choices=LISTA_OPERACOES)
    valor_unitario = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    custos_transacao = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    ir_fonte = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    quantidade = models.DecimalField(max_digits=15,
                                decimal_places=10,
                                default=0)
    
    
    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        if self.ativo_perfil_caixa.ativo.ticket == '':
            return (self.ativo_perfil_caixa.corretora.nome + ' - ' + 
                self.ativo_perfil_caixa.ativo.nome + ': ' + 
                self.data.strftime(f"%Y-%m-%d")) 
        else:
            return (self.ativo_perfil_caixa.corretora.nome + ' - ' + 
                self.ativo_perfil_caixa.ativo.ticket + ': ' + 
                self.data.strftime(f"%Y-%m-%d")) 

    def total(self):
        if self.operacao == ('VENDA' or 'Venda'):
            return self.quantidade * (self.valor_unitario - self.custos_transacao)
        else:
            return self.quantidade * (self.valor_unitario + self.custos_transacao)


class PosicaoData(models.Model):
    """
    Nesta tabela são armazenados as atualizações de valor dos investimentos, viabilizando a análise histórica.
    """
    ativo_perfil_caixa = models.ForeignKey('AtivoPerfilCaixa', 
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
    cota_sistema_valor = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)
    # valor dividendos recebidos
    dividendos = models.DecimalField(max_digits=19, 
                       decimal_places=4, 
                       default=0)

    def __str__(self) -> str:
        """
            Altera o nome padrão de exibição do objeto da classe.
        """
        
        if self.ativo_perfil_caixa.ativo.ticket == '':
            return (self.ativo_perfil_caixa.corretora.nome + ' - ' + 
                self.ativo_perfil_caixa.ativo.nome + ': ' + 
                self.data.strftime(f"%Y-%m-%d")) 
        else:
            return (self.ativo_perfil_caixa.corretora.nome + ' - ' + 
                self.ativo_perfil_caixa.ativo.ticket + ': ' + 
                self.data.strftime(f"%Y-%m-%d"))  