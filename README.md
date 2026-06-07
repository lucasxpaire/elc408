# Compilador Homi

Este repositório contém a implementação do Compilador para a linguagem **Homi**, desenvolvido para a disciplina de Compiladores. A linguagem converte instruções declarativas em português para o formato de automações YAML do Home Assistant.

## Estrutura do Projeto
- `main/`: Contém todo o código-fonte do compilador.
  - `analisadores/`: Implementações do Léxico, Sintático e Semântico.
  - `geradores/`: Lógica de conversão para YAML.
  - `inputs/`: Scripts Homi para testes (incluindo exemplos válidos e com erros).
  - `outputs/`: Diretório onde o YAML gerado será salvo.
  - `main.py`: Arquivo principal (Entrypoint).
- `documentacoes/`: Contém o Relatório Técnico LaTeX detalhando a implementação do projeto.

## Requisitos
- Python 3.8 ou superior.
- Nenhuma biblioteca externa é necessária (projeto desenvolvido inteiramente com as bibliotecas padrão do Python).

## Como Executar

Você pode executar o compilador de duas formas:

### Opção 1: Via Makefile
Na raiz do projeto, o arquivo `Makefile` fornece atalhos rápidos de execução:
- `make run`: Roda o compilador utilizando o script de teste padrão.
- `make test-lexico`: Roda o compilador forçando o erro léxico.
- `make test-sintatico`: Roda o compilador forçando o erro sintático (Modo Pânico).
- `make test-semantico`: Roda o compilador forçando o erro semântico.

### Opção 2: Via linha de comando (Python)
Para compilar um arquivo específico, navegue até a pasta `main/` e execute:
```bash
python main.py inputs/seu_arquivo.homi
```
Se executado sem argumentos, o `main.py` buscará automaticamente o arquivo `inputs/test_padrao.homi`.

## Onde encontrar o resultado?
Caso o arquivo de entrada seja processado sem erros léxicos, sintáticos ou semânticos, o arquivo final convertido será gerado na pasta `main/outputs/saida.yaml`.
