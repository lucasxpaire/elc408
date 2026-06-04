# Código: gerador.py

```python
yaml_final = "\n".join(self.linhas_yaml)
```
Nós adotamos a técnica de colocar todas as linhas num gigantesco vetor `self.linhas_yaml` e, no final de tudo, unir (Join) colocando quebras de linhas `\n` para evitar problemas de identação ao colar o texto num arquivo.

## As Traduções (O De/Para)
O Python viaja na árvore (assim como o Semântico fez). Ele possui lógicas simples como:
```python
estado_en = 'on' if estado_pt in ['ligado', 'aberto', 'movimento'] else 'off'
```

## A Geração de Comandos
```python
if verbo == 'ligar':
    dominio = alvo.split('.')[0]
    self.linhas_yaml.append(f"  - service: {dominio}.turn_on")
```
Para traduzir `ligar light.sala` para `light.turn_on`, nós quebramos a string alvo pelo ponto (`.`), pegamos a primeira parte (índice 0, o `light`) e colocamos no formato exato que os manuais do Home Assistant pedem.