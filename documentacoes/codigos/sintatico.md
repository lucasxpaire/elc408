# Código: sintatico.py

## A Tabela e a Pilha
```python
self.pilha = ['$', 'Programa']
self.tabela = {
    'BlocoQuando': {
        'QUANDO': ['QUANDO', 'RegraGatilho']
    }
}
```
Iniciamos a pilha com o símbolo de final de arquivo e a Regra Raiz (`Programa`). 
Dentro do laço `while len(self.pilha) > 0:`, se tirarmos o `BlocoQuando` do topo da pilha, e a palavra sendo lida naquele momento no arquivo for `QUANDO`, nós consultamos a Tabela Preditiva. Ela nos diz para empilhar de trás para frente a `RegraGatilho` e depois o terminal `QUANDO`.

## A Montagem da AST
```python
producao = self.tabela[topo][tipo_token_lido]
for simbolo in reversed(producao):
    self.pilha.append((simbolo, filho_node))
```
A grande sacada de código aqui foi fazer a `self.pilha` parar de guardar apenas strings, e passar a guardar **Tuplas** contendo a Regra e o Objeto da Árvore associado à ela. Assim, à medida que a gramática se ramifica, os nós da árvore também se grudam.

## O Modo Pânico
```python
def modo_panico(self, tokens_sincronizacao):
```
Se não dermos match, chamamos essa função passando Tokens âncoras (como `SE`, `ENTAO`, `EOF`). O Sintático vai consumir tokens do léxico eternamente até bater com uma dessas âncoras. Depois ele ativa `self.teve_erro = True` e tenta prosseguir.