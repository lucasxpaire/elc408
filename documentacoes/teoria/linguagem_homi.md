# Teoria: A Linguagem Homi

A linguagem Homi foi construída como uma DSL (Domain Specific Language) — uma linguagem focada num nicho bem restrito. Ela oculta a complexidade brutal da declaração YAML do Home Assistant e permite que leigos programem automações em português estruturado.

A linguagem divide o fluxo de pensamento em 3 pilares absolutos e inquebráveis:

### 1. QUANDO (O Gatilho / Trigger)
O gatilho diz ao sistema quando a automação deve acordar.
Pode ser temporal ou baseado no estado de um equipamento.
```homi
QUANDO horario 18:00
# ou
QUANDO tempo 5min
# ou
QUANDO sensor.porta for aberto
```

### 2. SE (A Condição / Condition)
A condição atua como um filtro. A automação acordou, mas só vai prosseguir se este filtro permitir. É possível unir múltiplas condições usando `E` ou `OU`.
```homi
SE light.sala_estar estiver desligado
E switch.tv estiver desligado
```

### 3. ENTAO (A Ação / Action)
O resultado final. O que a casa fará fisicamente no ambiente. Podem ser múltiplos comandos em fila.
```homi
ENTAO ligar light.quarto
E notificar "Modo noturno ativado"
```