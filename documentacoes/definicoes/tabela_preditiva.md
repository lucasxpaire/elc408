# Tabela Preditiva LL(1) Formal

A Tabela Preditiva é usada pelo Analisador Sintático Preditivo Top-Down. Ela é uma matriz onde a `Linha` é a regra que estamos tentando resolver (O Topo da Pilha) e a `Coluna` é a palavra que estamos lendo na string.

| Pilha (Não-Terminal) | Lendo 'QUANDO' | Lendo 'horario' | Lendo 'SE' | Lendo 'ligar' | ... |
|----------------------|----------------|-----------------|------------|---------------|-----|
| **BlocoQuando** | QUANDO RegraGatilho | - | - | - |
| **RegraGatilho** | - | TIPO_GATILHO Comp | - | - |
| **BlocoSe** | - | - | SE RegraCond | - |
| **Comando** | - | - | - | ACAO Comp|

Quando a interseção está vazia, há um Erro de Sintaxe (ou Modo Pânico é acionado).
Na implementação Python (`sintatico.py`), essa matriz foi construída usando Dicionários embutidos de rápida pesquisa. 