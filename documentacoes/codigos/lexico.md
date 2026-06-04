# Código: lexico.py

## As Regras (TOKEN_REGEX)
```python
TOKEN_REGEX = [
    ('AUTOMACAO', r'\bAUTOMACAO\b'),
    ('VERBO_ACAO',r'\b(ligar|desligar|alternar|notificar)\b'),
    # ...
]
```
A ordem aqui é extremamente importante. Palavras mais específicas e reservadas sempre devem vir antes. Por exemplo, se colocássemos a regra de qualquer texto genérico (ID_ENTIDADE) antes de VERBO_ACAO, o código acharia que a palavra "ligar" era o nome de uma entidade.

## O Laço Principal
```python
for match in re.finditer(regex_combinada, codigo_fonte):
```
O `re.finditer` varre todo o código do usuário e entrega cada achado na variável `match`. 
Usamos `match.lastgroup` para saber qual regra o identificou (ex: `VERBO_ACAO`) e `match.group()` para pegar o texto puro (ex: "ligar").

## A Trava de Segurança
```python
elif tipo_token == 'ERRO':
    print(f"[ERRO LÉXICO]...")
    teve_erro = True
```
Quando o regex cai no último item (`ERRO`, que é um simples ponto `r'.'` que consome qualquer caractere que não deu match em nada), nós ativamos a trava `teve_erro = True`. O laço não sofre `break` para podermos pegar todos os erros de uma vez na tela, mas no fim da função, ele entrega ao Orquestrador que aquele arquivo não é digno de ir pro Sintático.