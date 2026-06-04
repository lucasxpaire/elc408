# Teoria: Analisador Léxico

A Análise Léxica é a primeira fase do nosso compilador. O objetivo dela não é entender se o código faz sentido, mas sim atuar como um "Leitor de Palavras" que separa o texto cru em pedaços lógicos.

## O que usamos no trabalho:
1. **Expressões Regulares (Regex):** 
   Não usamos ferramentas externas prontas de compiladores; usamos a biblioteca nativa `re` do Python. O Regex atua nos bastidores simulando um Autômato Finito (uma máquina de estados que lê letra por letra). Por exemplo, a regra `\b(ligar|desligar)\b` é um autômato que aceita apenas essas duas palavras. Se ele as encontrar, gera um pacote com a etiqueta (Token) de nome `VERBO_ACAO`.

2. **Eliminação de Ruídos:** 
   O texto que o usuário digita vem sujo (com espaços, tabs, quebras de linha e comentários iniciados por `#`). A teoria léxica dita que espaços em branco não devem chegar na próxima fase, então nosso compilador simplesmente ignora esses ruídos e não gera Tokens para eles.

3. **Captura de Erros:**
   Para tornar nosso compilador resiliente, em vez do programa dar *crash* quando o usuário digita um caractere inválido (ex: `@`), usamos um "Catch-All" (uma regra genérica) no final. Essa regra captura o caractere maldito, gera um token especial de `ERRO`, avisa o usuário da linha onde ocorreu, e sinaliza ao compilador para abortar as próximas fases.