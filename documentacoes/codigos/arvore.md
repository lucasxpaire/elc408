# Código: arvore.py

```python
class CSTNode:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []
```

### Explicação dos Campos:
1. **`tipo`**: Guarda a qual regra aquele bloco pertence (Ex: `BlocoQuando`, ou `TIPO_GATILHO`).
2. **`valor`**: Usado para folhas (os nós que ficam na ponta da árvore). Quando um Terminal do Sintático consome uma palavra, ele guarda a palavra em si aqui (Ex: `ligar`).
3. **`filhos`**: Uma simples lista (vetor) do Python. É aqui que está o segredo estrutural. Um nó "Comando" terá em sua lista de filhos dois outros `CSTNode`s menores (O A��o e o Complemento).

Com essas poucas linhas e as invocações recursivas nos outros arquivos, recriamos uma Árvore Sintática (AST) plenamente capaz.