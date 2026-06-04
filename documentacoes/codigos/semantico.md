# Código: semantico.py

## A Construção do Contexto (Mocks)
No `__init__`, nós construímos o dicionário `self.tabela_simbolos`. 
- `acoes_permitidas`: Define que luzes podem sofrer 'ligar/desligar', mas sensores sofrem vazia `[]` pois apenas leem o ambiente.
- `estados_permitidos`: Sensores podem sentir `aberto`, mas lâmpadas sentem `ligado`.

## A Viagem na AST
```python
def percorrer_arvore(self, no):
    if no.tipo == 'Comando':
        self.validar_comando(no)
        
    for filho in no.filhos:
        self.percorrer_arvore(filho)
```
Ela pega o nó pai, verifica, e manda ela mesma verificar todos os nós filhos até chegar no fim da árvore.

## A Validação Segura
```python
for filho in no_comando.filhos:
    if filho.tipo == 'ACAO':
        a��o_node = filho
```
O método `validar_comando` apenas busca os filhos dentro dessa "caixa", pega o nome da entidade, valida no dicionário, pega o a��o, cruza com a restrição, e reporta o erro caso haja quebra da regra de negócio.