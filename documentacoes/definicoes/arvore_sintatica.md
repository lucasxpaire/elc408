# Definição Formal: Árvore Sintática

A Árvore Sintática (também conhecida como AST ou CST) é o código convertido da sua forma de texto sequencial para a forma estruturada hierárquica.

No nosso compilador, quando o usuário escreve: `ENTAO ligar light.quarto`, a estrutura montada em memória é a seguinte:

```text
                  [BlocoEntao]
                   /        \
               [ENTAO]    [Comando]
                          /      \
                [VERBO_ACAO]   [Complemento]
                  (ligar)           |
                              [ID_ENTIDADE]
                             (light.quarto)
```
