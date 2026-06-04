# Definição Formal: Gramática (GLC)

A Gramática Livre de Contexto (GLC) oficial atualizada da linguagem Homi.

### Notação e Regras
Maiúsculas/Minúsculas denotam Não-Terminais. 
MAIÚSCULAS fixas denotam Tokens Terminais (Ex: `AUTOMACAO`).
`ε` significa Epsilon (transição vazia/opcional).

```text
Programa -> AUTOMACAO STRING BlocoQuando BlocoSe BlocoEntao

BlocoQuando -> QUANDO RegraGatilho

RegraGatilho -> TIPO_GATILHO ComplementoGatilho
             | ID_ENTIDADE OPERADOR ESTADO

ComplementoGatilho -> TEMPO_EXATO 
                   | TEMPO_UNIT

BlocoSe -> SE RegraCondicao 
        | ε

RegraCondicao -> ID_ENTIDADE OPERADOR ESTADO MaisCondicoes

MaisCondicoes -> OP_LOGICO RegraCondicao 
              | ε

BlocoEntao -> ENTAO Comando MaisComandos

Comando -> VERBO_ACAO Complemento

Complemento -> ID_ENTIDADE 
            | STRING

MaisComandos -> OP_LOGICO Comando MaisComandos 
             | ε
```
