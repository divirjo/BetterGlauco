from datetime import datetime
from decimal import Decimal

import pandas as pd
import pytz

from investimento.models import AtivoPerfilCaixa, ExtratoOperacao, TipoOperacao


class registrar_nota_corretagem:
    _id = 0

    id_linha_selecionada = -1

    _data = str(datetime.now().strftime(r'%d/%m/%Y'))

    _total_custos = 0

    _ir_fonte = 0

    _operacoes = TipoOperacao.choices

    _df_nota_corretagem = pd.DataFrame()

    _linha_df_nota_corretagem = {
        'id': 0,
        'ativo_perfil_caixa_id': 0,
        'ativo_ticket': '',
        'ativo_nome': '',
        'data': '',
        'operacao': '',
        'quantidade': Decimal(0),
        'valor_unitario': Decimal(0),
        'custo_unitario_transacao': Decimal(0),
        'total': Decimal(0),
        'ir_fonte_unitario': Decimal(0),
    }

    def __init__(self):
        self.nova_nota_corretagem()

    def get_dict_nota_corretagem(self):
        return self._df_nota_corretagem.to_dict('records')

    def get_quantidade_total(self):
        return Decimal(self._df_nota_corretagem['quantidade'].sum())

    def get_total_operacao_sem_custos(self):
        sr_total_operacao = (
            self._df_nota_corretagem['quantidade']
            * self._df_nota_corretagem['valor_unitario']
        )

        return Decimal(sr_total_operacao.sum())

    def get_total_vendas_sem_custos(self):
        df_total_operacao = self._df_nota_corretagem.groupby('operacao').apply(
            lambda x: x['quantidade'] * x['valor_unitario']
        )

        if not df_total_operacao.empty:
            resultado_venda = df_total_operacao.loc['VENDA']
            total_vendas = resultado_venda.sum()
        else:
            total_vendas = 0

        return Decimal(total_vendas)

    def distribuir_custos_nota(self):
        total_operacao = self.get_total_operacao_sem_custos()

        for indice, linha in self._df_nota_corretagem.iterrows():
            subtotal_operacao_sem_custos = (
                linha['quantidade'] * linha['valor_unitario']
            )

            custo_ativo_transacao = (
                subtotal_operacao_sem_custos
                / total_operacao
                * self._total_custos
            )

            custo_unitario_transacao = Decimal(
                custo_ativo_transacao / linha['quantidade']
            )

            if linha['operacao'] == TipoOperacao.VENDA:
                total_ativo = (
                    linha['valor_unitario'] - custo_unitario_transacao
                ) * linha['quantidade']
            else:
                total_ativo = (
                    linha['valor_unitario'] + custo_unitario_transacao
                ) * linha['quantidade']

            self._df_nota_corretagem.at[indice, 'custo_unitario_transacao'] = (
                custo_unitario_transacao
            )

            self._df_nota_corretagem.at[indice, 'total'] = Decimal(total_ativo)

    def distribuir_ir_fonte(self):
        if (
            not self._df_nota_corretagem['operacao']
            .str.contains(TipoOperacao.VENDA)
            .any()
        ):
            return

        total_vendas = self.get_total_vendas_sem_custos()

        for indice, linha in self._df_nota_corretagem.iterrows():
            if not (linha['operacao'] == TipoOperacao.VENDA):
                continue

            subtotal_operacao_sem_custos = (
                linha['quantidade'] * linha['valor_unitario']
            )

            ir_transacao = (
                subtotal_operacao_sem_custos / total_vendas * self._ir_fonte
            )

            self._df_nota_corretagem.at[indice, 'ir_fonte'] = Decimal(
                ir_transacao
            )

    def alterar_ativo_nota(
        self, ativo_perfil_caixa_id, operacao, quantidade, valor_unitario
    ):
        linha = self._linha_df_nota_corretagem.copy()

        linha['id'] = self.id_linha_selecionada
        linha['ativo_perfil_caixa_id'] = int(ativo_perfil_caixa_id)

        ativo_selecionado = AtivoPerfilCaixa.objects.filter(
            id=ativo_perfil_caixa_id
        ).values('ativo__ticket', 'ativo__nome')

        linha['ativo_ticket'] = ativo_selecionado[0]['ativo__ticket']
        linha['ativo_nome'] = ativo_selecionado[0]['ativo__nome']
        linha['data'] = self._data
        linha['operacao'] = operacao
        linha['quantidade'] = Decimal(quantidade)
        linha['valor_unitario'] = Decimal(valor_unitario)

        self._df_nota_corretagem.loc[self.id_linha_selecionada] = linha

        self.distribuir_custos_nota()

    def incluir_ativo_nota(
        self, ativo_perfil_caixa_id, operacao, quantidade, valor_unitario
    ):
        nova_linha = self._linha_df_nota_corretagem.copy()

        nova_linha['id'] = self._id
        self._id += 1

        nova_linha['ativo_perfil_caixa_id'] = int(ativo_perfil_caixa_id)

        ativo_selecionado = AtivoPerfilCaixa.objects.filter(
            id=ativo_perfil_caixa_id
        ).values('ativo__ticket', 'ativo__nome')

        nova_linha['ativo_ticket'] = ativo_selecionado[0]['ativo__ticket']
        nova_linha['ativo_nome'] = ativo_selecionado[0]['ativo__nome']

        nova_linha['data'] = self._data
        nova_linha['operacao'] = operacao
        nova_linha['quantidade'] = Decimal(quantidade)
        nova_linha['valor_unitario'] = Decimal(valor_unitario)

        self._df_nota_corretagem.loc[len(self._df_nota_corretagem)] = (
            nova_linha
        )

        self.distribuir_custos_nota()

    def nova_nota_corretagem(self):
        self._id = 0
        self._ir_fonte = 0
        self._total_custos = 0
        self._df_nota_corretagem = pd.DataFrame(
            columns=[
                'id',
                'ativo_perfil_caixa_id',
                'ativo_ticket',
                'ativo_nome',
                'data',
                'operacao',
                'quantidade',
                'valor_unitario',
                'custo_unitario_transacao',
                'total',
                'ir_fonte_unitario',
            ]
        )

    def salvar_operacoes_nota(self):
        if len(self._df_nota_corretagem) == 0:
            return 'Nenhum ativo foi incluído'
        else:
            mensagem_retorno = 'Ativos incluídos com sucesso:'

        sao_paulo_tz = pytz.timezone('America/Sao_Paulo')

        for indice, linha in self._df_nota_corretagem.iterrows():
            ativo_perfil_caixa = AtivoPerfilCaixa.objects.get(
                id=int(linha['ativo_perfil_caixa_id'])
            )

            operacao = ExtratoOperacao(
                ativo_perfil_caixa=ativo_perfil_caixa,
                data=sao_paulo_tz.localize(linha['data']),
                operacao=linha['operacao'],
                valor_unitario=Decimal(linha['valor_unitario']),
                custos_transacao=Decimal(linha['custo_unitario_transacao']),
                ir_fonte=Decimal(linha['ir_fonte_unitario']),
                quantidade=Decimal(linha['quantidade']),
            )
            operacao.save()

            if len(linha['ativo_ticket']) > 0:
                mensagem_retorno += ' {},'.format(linha['ativo_ticket'])
            else:
                mensagem_retorno += ' {},'.format(linha['ativo_nome'])

        self.nova_nota_corretagem()

        return mensagem_retorno

    def set_data_nota(self, data):
        self._data = data
        self._df_nota_corretagem['data'] = data

    def set_total_custos(self, total_custos):
        if self._total_custos != total_custos:
            self._total_custos = total_custos
            self.distribuir_custos_nota()
        else:
            self._total_custos = total_custos

    def set_ir_fonte(self, ir_fonte):
        if self._ir_fonte != ir_fonte:
            self._ir_fonte = ir_fonte
            self.distribuir_ir_fonte()
        else:
            self._ir_fonte = ir_fonte
