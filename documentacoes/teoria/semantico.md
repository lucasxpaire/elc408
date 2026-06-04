# Teoria: Analisador Semântico

O Analisador Sintático aceitaria tranquilamente a frase: *"O microondas tomou banho"*. A gramática está certa (Sujeito + A��o + Objeto). É a Análise Semântica que proíbe isso verificando as regras lógicas e do mundo real.

## O que usamos no trabalho:
1. **Navegação na Árvore (Visitor):**
   Nós não lemos mais a lista de palavras em texto. Nós viajamos pela Árvore Sintática (AST). Ao entrar no galho pai "Comando", sabemos que o galho filho "A��o" pertence indiscutivelmente ao galho filho "Alvo".

2. **Tabela de Símbolos (Mocks):**
   Em compiladores reais (como C ou Java), a tabela de símbolos guarda os nomes das variáveis e seus tipos (int, string). No nosso compilador, a Tabela de Símbolos guarda as entidades do Home Assistant (`light.sala_estar`) e o domínio delas (`light`). Como não estamos de fato conectados na rede da casa do usuário, nós "Mockamos" (simulamos) essa tabela.

3. **Análise de Contexto / Restrições:**
   - **Ação vs Entidade:** Cruzamos o A��o (ex: `ligar`) com as `acoes_permitidas` para o domínio (sensores não podem ser ligados).
   - **Estado vs Entidade:** Cruzamos o Estado verificado (ex: `movimento`) com os `estados_permitidos` para garantir que apenas sensores de porta (binary_sensor) testem esse status.

## Os Pilares da Nossa Semântica (Vocabulário do Home Assistant)
Para o compilador conseguir fazer essas validações (explicadas no tópico 3), nós tivemos que modelar os conceitos reais do sistema alvo. No nosso analisador semântico existem 4 elementos centrais:

1. **Entidade (Entity):** É o objeto físico ou virtual específico. É a string completa. 
   - *Exemplo:* `light.sala_estar`, `sensor.temperatura`
2. **Domínio (Domain):** É a "Classe" ou a "Família" do objeto. Todo objeto no Home Assistant tem seu domínio escrito antes do ponto final. O compilador usa o domínio para saber a natureza do objeto.
   - *Exemplo:* Em `light.quarto`, o domínio é `light` (luz). Em `binary_sensor.porta`, o domínio é `binary_sensor` (sensor de dois estados).
3. **Estado (State):** É a condição atual que a entidade "sente" ou se encontra. É usado na parte do `SE`. 
   - *Exemplo:* Uma porta (domínio `binary_sensor`) suporta o estado `aberto` ou `fechado`. Uma luz não suporta isso, ela só suporta os estados `ligado` e `desligado`.
4. **A��o/Ação (Service):** É o comando que a automação vai obrigar a entidade a realizar. É usado na parte do `ENTAO`.
   - *Exemplo:* Uma luz (domínio `light`) suporta a ação `ligar`, `desligar` ou `alternar`. Um sensor (domínio `sensor`) suporta ZERO ações. Ninguém pode "mandar" num termômetro, ele apenas afere o ambiente.

O objetivo único do `AnalisadorSemantico` é garantir que as **Ações** e os **Estados** solicitados no código da automação são matematicamente compatíveis com o **Domínio** da **Entidade** mencionada.