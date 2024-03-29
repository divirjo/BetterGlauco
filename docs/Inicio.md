## Início do sistema

Para auxiliar na construção dos fluxos em markdown, estamos utilizando o [Mermaid](https://www.mermaidchart.com/)

# área pública

# área interna

```mermaid
    flowchart TD
        1[Início] --> 2(Investimento)
            2 --> 2.1[Alocação]
            2 --> 2.2[Registrar compra]
            2 --> 2.3[Atualização]
            2 --> 2.4[Análise]
        1 --> 3{BRD}
            3 --> 3.1[Valor compra]
            3 --> 3.2[Cálculo imposto retido USA]
        1 --> 4[Configurações]
            4 --> 4.1[cadastro ativos]
            4 --> 4.2[acesso admin django]
        1 --> 5[Ajuda]
```

Módulos:
* Cadastro das compras e vendas realizadas: [Operações](/docs/modulo_operacoes.md)
* Cadastro dos preços dos ativos: [Atualização](/docs/modulo_atualizacao.md)