# Teoria: Analisador Semântico

O Analisador Sintático aceitaria tranquilamente a frase: *"O microondas tomou banho"*. A gramática está certa (Sujeito + Verbo + Objeto). É a Análise Semântica que proíbe isso verificando as regras lógicas e do mundo real.

## O que usamos no trabalho:
1. **Navegação na Árvore (Visitor):**
   Nós não lemos mais a lista de palavras em texto. Nós viajamos pela Árvore Sintática (AST). Ao entrar no galho pai "Comando", sabemos que o galho filho "Verbo" pertence indiscutivelmente ao galho filho "Alvo".

2. **Tabela de Símbolos (Mocks):**
   Em compiladores reais (como C ou Java), a tabela de símbolos guarda os nomes das variáveis e seus tipos (int, string). No nosso compilador, a Tabela de Símbolos guarda as entidades do Home Assistant (`light.sala_estar`) e o domínio delas (`light`). Como não estamos de fato conectados na rede da casa do usuário, nós "Mockamos" (simulamos) essa tabela.

3. **Análise de Contexto / Restrições:**
   - **Ação vs Entidade:** Cruzamos o Verbo (ex: `ligar`) com as `acoes_permitidas` para o domínio (sensores não podem ser ligados).
   - **Estado vs Entidade:** Cruzamos o Estado verificado (ex: `movimento`) com os `estados_permitidos` para garantir que apenas sensores de porta (binary_sensor) testem esse status.