# Módulo Atualização

Atualização da posição dos ativos, com as cotações do dia cadastrado. 

É possível cadastrar manualmente uma posição, quanto cadastrar a posição automaticamente.


```mermaid
 1[Módulo atualizar cotação ativos] --> 2(Página inicial)
        2 --> 2.1[Exibir as atualizações mais recentes de cada artigo]

    1 --> 3[Atualizar por ativo fundo]
        3 --> 3.0[Exibir as operações mais recentes]
            3.0 --> 3.1.1[atualizar operação]
        3.0 --> 3.1[filtrar por ativo cadastrado no perfil]
            3.1 --> 3.1.1[atualizar operação]
                 3.1.1 --> 3.1.2[carregar campos]
                 3.1.2 --> 3.1.3[usuário atualiza campos]

        3 --> 3.2[Cadastrar nova posição]
    
    1 --> 6[Atualizar por ativo bolsa]
        6 --> 6.0[Exibir as operações mais recentes]
            6.0 --> 6.1.1[atualizar operação]
            6.0 --> 6.1[filtrar por ativo]
                6.1 --> 6.1.1[atualizar operação]
                    6.1.1 --> 6.1.2[carregar campos]
                    6.1.2 --> 6.1.3[usuário atualiza campos]

        6 --> 6.2[Cadastrar nova posição]
        6 --> 6.3[Atualizar valores automaticamente]

    1 --> 4[Atualizar bolsa automático]
        4 --> 4.0[Exibir as operações mais recentes]
            4.0 --> 4.1.1[atualizar operação]
            4.0 --> 4.1[filtrar por corretora]
                4.1 --> 4.1.1[atualizar operação]
                    4.1.1 --> 4.1.2[carregar campos]
                    4.1.2 --> 4.1.3[usuário atualiza campos]
                4.1 --> 4.2[Cadastrar nova posição]

    1 --> 5[Incluir dividendos]
        5 --> 5.1[Exibir somente ativos do perfil e que pagam dividendos]
```

## cálculo do valor do ativo
O cálculo do valor do ativo é realizado pela operação:

valor_atual = quantidade_cotas x valor_cota

## atualização do valor do ativo
O usuário pode informar o valor da cota, nesse caso basta salvar o valor informado.

Caso o usuário informe o valor total da posição, para salvar é necessário dividir pelo valor das cotas.

É importante considerar que o valor pode estar em reais ou em dólares. Para cálculo de ativos internacionais, é importante armazenar o valor em reais e o valor em dólares no dia.

## cotação dos ativos em bolsa
A posição dos ativos será salva em duas planilhas, pois a cotação dos ativos que estão na bolsa de valores é a mesma para todos os usuários do sistema.

Apesar de que deveria ocorrer a mesma coisa com as cotas de fundo de investimento, é necessário considerar que nem todo banco ou corretora divulga o valor exato das cotas que o usuário possui, o que poderia gerar erros ao vincular todos os ativos à tabela de fundos.
