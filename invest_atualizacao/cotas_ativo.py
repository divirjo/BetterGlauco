from django.db.models import Sum

from BetterGlauco.parametro import Constante
from investimento.models import (
    Ativo,
    ExtratoOperacao,
    PosicaoDataBolsa,
    PosicaoDataFundo,
    TipoOperacao,
)


class CotaAtivo:
    _CONSTANTE = Constante()

    def __init__(self, ativo_id):
        self._ativo = Ativo.objects.get(id=ativo_id)

    def quantidadeTotal(self):
        total_adquirido = (
            ExtratoOperacao.objects.filter(
                ativo_perfil_caixa__ativo_id=self._ativo.id
            )
            .exclude(operacao=TipoOperacao.VENDA)
            .aggregate(Sum('quantidade'))
        )
        if total_adquirido['quantidade__sum'] is None:
            total_adquirido['quantidade__sum'] = 0

        total_vendido = ExtratoOperacao.objects.filter(
            ativo_perfil_caixa__ativo_id=self._ativo.id,
            operacao=TipoOperacao.VENDA,
        ).aggregate(Sum('quantidade'))
        if total_vendido['quantidade__sum'] is None:
            total_vendido['quantidade__sum'] = 0

        saldo_cotas = (
            total_adquirido['quantidade__sum']
            - total_vendido['quantidade__sum']
        )

        return saldo_cotas

    def valorMaisRecente(self):
        valorCota = self._CONSTANTE.VALOR_PADRAO_COTA()

        if self._ativo.cota_bolsa:
            posicaoAtivo = (
                PosicaoDataBolsa.objects.filter(ativo=self._ativo.id)
                .order_by('-data')
                .first()
            )
            if posicaoAtivo:
                valorCota = posicaoAtivo.cota_valor
        else:
            posicaoAtivo = (
                PosicaoDataFundo.objects.filter(
                    ativo_perfil_caixa__ativo=self._ativo.id
                )
                .order_by('-data')
                .first()
            )
            if posicaoAtivo:
                valorCota = posicaoAtivo.cota_sistema_valor

        return valorCota
