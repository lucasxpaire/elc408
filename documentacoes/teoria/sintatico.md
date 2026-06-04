# Teoria: Analisador Sintático

A Análise Sintática verifica a estrutura gramatical do que foi digitado. Ela pergunta: "As palavras estão na ordem correta segundo as regras da linguagem?".

## O que usamos no trabalho:
1. **Gramática Livre de Contexto (GLC):** 
   É o conjunto de regras que inventamos. Ela diz que um `BlocoQuando` tem que ser seguido pela palavra `QUANDO` e depois por uma `RegraGatilho`. 

2. **Parser Top-Down LL(1):**
   Existem várias formas de analisar gramática. Nós usamos a **Preditiva LL(1)**. 
   - **Top-Down:** Começamos pela regra mais alta (a raiz `Programa`) e vamos derivando até chegar nas palavras miúdas.
   - **LL(1):** Lemos o texto da Esquerda para a Direita (L), pegamos a derivação mais à Esquerda (L) e precisamos olhar apenas **1** palavra (Token) para frente para saber qual regra usar. Não tentamos adivinhar ou voltar atrás (backtracking).

3. **Tabela Preditiva e Pilha:**
   Para não termos dezenas de `if/else`, colocamos as regras num mapa bidimensional. Usamos uma estrutura de dados de **Pilha** (LIFO - Last In, First Out). Empilhamos o que esperamos ler. Se o que está no topo da pilha é igual à palavra sendo lida, nós "casamos" (Match) e jogamos os dois fora.

4. **Árvore Sintática Abstrata (AST):**
   Ao mesmo tempo que desempilhamos as regras, criamos pequenos blocos de dados (`CSTNode`) e penduramos uns nos outros. A árvore elimina a necessidade da ordem sequencial e cria uma hierarquia perfeita para a próxima fase ler.

5. **Recuperação de Erros (Modo Pânico):**
   Se o usuário errar a digitação, não fechamos o compilador. Nós entramos no **Modo Pânico**: começamos a jogar palavras fora até encontrarmos uma palavra "segura" (como `SE` ou `ENTAO`). A partir daí, tentamos continuar a análise para achar outros erros no final do texto.