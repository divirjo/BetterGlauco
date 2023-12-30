from investimento.models import AtivoPerfilCaixa

class TabelaAlocacao():
    
    tabela_alocacao_teorica = {}
    linha = {'Caixa': '',
             'Subclasse': '',
             'Ativo': '',
             'Corretora': '',
             'Valor Alocação Teórica (R$)': '',
             'Alocação Teórica Caixa(%)': 0,
             'Alocação Teórica Carteira(%)': 0,
                 }
    perfil_usuario = 0
    
    def __init__(self, id_perfil_selecionado):
        self.perfil_usuario = id_perfil_selecionado
    
    def getTabelaAlocacaoTeorica(self):
        self.tabela_alocacao_teorica['header'] = self.linha.copy()
        total_alocacao_caixa = 0
        total_alocacao_carteira = 0
        caixa_anterior = ''

        consulta_bd = AtivoPerfilCaixa.objects.filter(subclasse__caixa__perfil=self.perfil_usuario).order_by('subclasse__caixa__ordem_exibicao','subclasse__caixa__nome', 'ativo__ticket','ativo__nome')
        
        for index, linha_consulta in enumerate(consulta_bd):
            linha_tabela = self.linha.copy()
            
            if index == 0:
                caixa_anterior = linha_consulta.subclasse.caixa.nome
                
            if caixa_anterior != linha_consulta.subclasse.caixa.nome:
                linha_tabela['Caixa'] = 'Total caixa ' + caixa_anterior
                linha_tabela['Alocação Teórica Caixa(%)'] = total_alocacao_caixa
                self.tabela_alocacao_teorica['Total Caixa' + caixa_anterior] = linha_tabela
                total_alocacao_caixa = 0
                caixa_anterior = linha_consulta.subclasse.caixa.nome
                linha_tabela = self.linha.copy()
            
            linha_tabela['Caixa'] = linha_consulta.subclasse.caixa.nome
            linha_tabela['Subclasse'] = linha_consulta.subclasse.nome
            linha_tabela['Ativo'] = linha_consulta.ativo
            linha_tabela['Corretora'] = linha_consulta.corretora
            if linha_consulta.alocacao_teorica_valor > 0:
                linha_tabela['Valor Alocação Teórica (R$)'] = linha_consulta.alocacao_teorica_valor
            linha_tabela['Alocação Teórica Caixa(%)'] = linha_consulta.aloc_teor_percent_caixa
            total_alocacao_caixa += linha_consulta.aloc_teor_percent_caixa
            linha_tabela['Alocação Teórica Carteira(%)'] = linha_consulta.aloc_teor_percent_carteira
            total_alocacao_carteira += linha_consulta.aloc_teor_percent_carteira
            self.tabela_alocacao_teorica[str(linha_consulta.id)] = linha_tabela
            
        linha_tabela = self.linha.copy()
        linha_tabela['Caixa'] = 'Total caixa ' + caixa_anterior
        linha_tabela['Alocação Teórica Caixa(%)'] = total_alocacao_caixa
        self.tabela_alocacao_teorica['Total Caixa' + caixa_anterior] = linha_tabela
        
        linha_tabela = self.linha.copy()
        linha_tabela['Caixa'] = 'Total alocação'
        linha_tabela['Alocação Teórica Caixa(%)'] = total_alocacao_caixa
        linha_tabela['Alocação Teórica Carteira(%)'] = total_alocacao_carteira
        self.tabela_alocacao_teorica['Total'] = linha_tabela
        
        
        return self.tabela_alocacao_teorica
    