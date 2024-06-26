from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TipoOperacao(models.TextChoices):
    VENDA = 'VENDA', 'Venda'
    COMPRA = 'COMPRA', 'Compra'
    SUBSCRICAO = 'SUBSCRIÇÃO', 'Subscrição'
    DESDOBRO = 'DESDOBRO', 'Desdobramento'


class Parametro(models.Model):
    """
    Model com as parametrizações do sistema
    """

    nome = models.CharField(
        max_length=100, unique=True, help_text='Nome da constante'
    )
    valor = models.TextField(default='', help_text='Valor da constante')
    descricao = models.TextField(
        default='', help_text='Descrição da constante'
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class Usuario(AbstractUser):
    observacao = models.TextField()


class Perfil(models.Model):
    usuarios_permitidos = models.ManyToManyField('Usuario')
    nome = models.CharField(
        max_length=25,
        help_text='Nome para identificar o perfil (conta de investimento',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class Ativo(models.Model):
    # Código da bolsa do ativo ou um apelido do fundo
    ticket = models.CharField(
        max_length=10,
        default='',
        blank=True,
        help_text='Código de negociação do ativo na bolsa',
    )
    nome = models.CharField(max_length=100, help_text='Nome do ativo')
    cnpj = models.CharField(
        max_length=19, default='', blank=True, help_text='CNPJ do ativo'
    )
    cota_bolsa = models.BooleanField(
        default=False, blank=False, help_text='O ativo possui cota na bolsa?'
    )
    dividendos = models.BooleanField(
        default=False, blank=False, help_text='O ativo distribui dividendos?'
    )

    # Parametrização BDRs (ativo referência e desdobramento)
    ticket_original = models.CharField(
        max_length=10,
        default='',
        blank=True,
        help_text='Código de negociação original do ativo (somente BDRs)',
    )
    desdobramento = models.DecimalField(
        max_digits=15,
        decimal_places=10,
        default=0,
        help_text='Quanto representa a cota brasileira em relação ao ativo \
            original (somente BDRs)',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """

        if not self.ticket:
            return self.nome
        else:
            return self.ticket + ': ' + self.nome


class AtivoPerfilCaixa(models.Model):
    subclasse = models.ForeignKey(
        'ClasseAtivo',
        related_name='ativos_subclasse',
        on_delete=models.DO_NOTHING,
    )
    ativo = models.ForeignKey(
        'Ativo', related_name='posicoes', on_delete=models.PROTECT
    )
    corretora = models.ForeignKey(
        'InstituicaoFinanceira',
        related_name='ativos',
        on_delete=models.DO_NOTHING,
    )
    alocacao_teorica_valor = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='Valor ideal de alocação no ativo',
    )
    aloc_teor_percent_caixa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Percentual ideal de alocação do ativo \
            em referência ao valor alocando na caixa',
    )
    aloc_teor_percent_carteira = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Percentual ideal de alocação do ativo \
            em referência ao total investido',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """

        if not self.ativo.ticket:
            return (
                self.subclasse.caixa.nome
                + ' - '
                + self.ativo.nome
                + ' ('
                + self.corretora.nome
                + ')'
            )
        else:
            return (
                self.subclasse.caixa.nome
                + ' - '
                + self.ativo.ticket
                + ' - '
                + self.ativo.nome
                + ' ('
                + self.corretora.nome
                + ')'
            )


class Caixa(models.Model):
    perfil = models.ForeignKey(
        'Perfil', related_name='caixas', on_delete=models.PROTECT
    )
    nome = models.CharField(max_length=100)

    ordem_exibicao = models.IntegerField(default=0)

    cota_sistema_valor = models.DecimalField(
        max_digits=19, decimal_places=4, default=0
    )
    alocacao_teorica_valor = models.DecimalField(
        max_digits=19, decimal_places=4, default=0
    )
    alocacao_teorica_percentual = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class ClasseAtivo(models.Model):
    caixa = models.ForeignKey(
        'Caixa', related_name='subclasses', on_delete=models.PROTECT
    )
    nome = models.CharField(max_length=100)
    alocacao_teorica_valor = models.DecimalField(
        max_digits=19, decimal_places=4, default=0
    )
    alocacao_teorica_percentual = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        return self.caixa.nome + ' - ' + self.nome


class Dividendos(models.Model):
    """
    Nesta tabela são armazenados os dividendos recebidos
    """

    ativo_perfil_caixa = models.ForeignKey(
        'AtivoPerfilCaixa', related_name='dividendos', on_delete=models.PROTECT
    )
    data = models.DateTimeField(default=timezone.now)
    dividendos = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='valor dividendos recebidos',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        if not self.ativo_perfil_caixa.ativo.ticket:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.nome
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )
        else:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.ticket
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )


class InstituicaoFinanceira(models.Model):
    nome = models.TextField(max_length=100)
    perfil = models.ForeignKey(
        'Perfil',
        related_name='instituicoes_financeiras',
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        return self.nome


class ExtratoOperacao(models.Model):
    """
    Model da tabela que discrimina as operações de compra e venda de ativos
    """

    ativo_perfil_caixa = models.ForeignKey(
        'AtivoPerfilCaixa',
        related_name='operacoes',
        on_delete=models.PROTECT,
        verbose_name='Ativo',
    )
    data = models.DateTimeField(default=timezone.now)
    operacao = models.CharField(
        max_length=10,
        choices=TipoOperacao.choices,
        verbose_name='Operação',
    )
    valor_unitario = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        verbose_name='Valor unitário',
    )
    custos_transacao = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        verbose_name='Custos de transação',
    )
    ir_fonte = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        verbose_name='Imposto de Renda retido na fonte',
    )
    quantidade = models.DecimalField(
        max_digits=15,
        decimal_places=10,
        default=0,
        verbose_name='Cotas',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """
        if not self.ativo_perfil_caixa.ativo.ticket:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.nome
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )
        else:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.ticket
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )

    def total(self):
        """
        Cria coluna calculada que representa o valor total da operação
        """
        if self.operacao == TipoOperacao.VENDA:
            return self.quantidade * (
                self.valor_unitario - self.custos_transacao
            )
        else:
            return self.quantidade * (
                self.valor_unitario + self.custos_transacao
            )


class PosicaoDataBolsa(models.Model):
    """
    Nesta tabela são armazenados as atualizações de valor
    dos investimentos listados em bolsa, viabilizando a análise histórica.
    """

    ativo = models.ForeignKey(
        'Ativo',
        related_name='posicoesBolsa',
        on_delete=models.PROTECT,
        verbose_name='Ativo',
    )
    data = models.DateTimeField(
        default=timezone.now,
        help_text='Data da atualização da cota',
        verbose_name='Data',
    )
    cota_valor = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='valor cota na bolsa',
        verbose_name='Valor cota (R$)',
    )
    cota_valor_dolar = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='valor em dolar da cota na bolsa \
            (investimentos internacionais)',
        verbose_name='Valor cota (US$)',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """

        if not self.ativo.ticket:
            return self.ativo.nome + ': ' + self.data.strftime('%Y-%m-%d')
        else:
            return (
                self.ativo.ticket
                + ' - '
                + self.ativo.nome
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )


class PosicaoDataFundo(models.Model):
    """
    Nesta tabela são armazenados as atualizações de valor dos
    investimentos não listados em bolsa, viabilizando a análise histórica.
    """

    ativo_perfil_caixa = models.ForeignKey(
        'AtivoPerfilCaixa',
        related_name='posicoes',
        on_delete=models.PROTECT,
        verbose_name='Ativo',
    )
    data = models.DateTimeField(
        default=timezone.now,
        help_text='Data da atualização da cota',
        verbose_name='Data',
    )
    cota_sistema_valor = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='valor cota do sistema',
        verbose_name='Valor cota (R$)',
    )
    cota_valor_dolar = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        help_text='valor em dolar da cota (investimentos internacionais)',
        verbose_name='Valor cota (US$)',
    )

    def __str__(self) -> str:
        """
        Altera o nome padrão de exibição do objeto da classe.
        """

        if not self.ativo_perfil_caixa.ativo.ticket:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.nome
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )
        else:
            return (
                self.ativo_perfil_caixa.corretora.nome
                + ' - '
                + self.ativo_perfil_caixa.ativo.ticket
                + ': '
                + self.data.strftime('%Y-%m-%d')
            )

    def cotas(self):
        """
        Cria coluna calculada que representa a quantidade de cotas do ativo
        """

        total_adquirido = (
            ExtratoOperacao.objects.filter(
                ativo_perfil_caixa__ativo=self.ativo_perfil_caixa.ativo,
            )
            .exclude(operacao=TipoOperacao.VENDA)
            .aggregate(models.Sum('quantidade'))
        )
        if total_adquirido['quantidade__sum'] is None:
            total_adquirido['quantidade__sum'] = 0

        total_vendido = ExtratoOperacao.objects.filter(
            ativo_perfil_caixa__ativo=self.ativo_perfil_caixa.ativo,
            operacao=TipoOperacao.VENDA,
        ).aggregate(models.Sum('quantidade'))
        if total_vendido['quantidade__sum'] is None:
            total_vendido['quantidade__sum'] = 0

        saldo_cotas = (
            total_adquirido['quantidade__sum']
            - total_vendido['quantidade__sum']
        )
        return saldo_cotas

    def total(self):
        """
        Cria coluna calculada que representa a quantidade de cotas do ativo
        """

        total = self.cota_sistema_valor * self.cotas()
        return total
