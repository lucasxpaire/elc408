from estruturas.arvore import CSTNode
from analisadores.lexico import Token

TOKEN_EOF = 'EOF'
SIMBOLO_FIM_PILHA = '$'

TERMINAIS = {
    'AUTOMACAO', 'QUANDO', 'SE', 'ENTAO', 'OP_LOGICO', 'ACAO', 'ESTADO', 
    'OPERADOR', 'TIPO_GATILHO', 'TEMPO_EXATO', 'TEMPO_UNIT', 'ID_ENTIDADE', 
    'STRING', TOKEN_EOF
}

class AnalisadorSintatico:
    def __init__(self, tokens):
        linha_fim = tokens[-1].linha if tokens else 1
        self.tokens = tokens + [Token(TOKEN_EOF, SIMBOLO_FIM_PILHA, linha_fim)]
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao]
        
        self.arvore = CSTNode('Programa')
        
        self.pilha = [(SIMBOLO_FIM_PILHA, None), ('Programa', self.arvore)]
        
        self.erros = []
        
        self.tabela = {
            'Programa': {
                'AUTOMACAO': ['AUTOMACAO', 'STRING', 'BlocoQuando', 'BlocoSe', 'BlocoEntao']
            },
            'BlocoQuando': {
                'QUANDO': ['QUANDO', 'RegraGatilho']
            },
            'RegraGatilho': {
                'TIPO_GATILHO': ['TIPO_GATILHO', 'ComplementoGatilho'],
                'ID_ENTIDADE': ['ID_ENTIDADE', 'OPERADOR', 'ESTADO']
            },
            'ComplementoGatilho': {
                'TEMPO_EXATO': ['TEMPO_EXATO'],
                'TEMPO_UNIT': ['TEMPO_UNIT']
            },
            'BlocoSe': {
                'SE': ['SE', 'RegraCondicao'],
                'ENTAO': [] # Transição Epsilon (ε): Se ler ENTAO, o BlocoSe acaba vazio
            },
            'RegraCondicao': {
                'ID_ENTIDADE': ['ID_ENTIDADE', 'OPERADOR', 'ESTADO', 'MaisCondicoes']
            },
            'MaisCondicoes': {
                'OP_LOGICO': ['OP_LOGICO', 'RegraCondicao'],
                'ENTAO': [] # Epsilon
            },
            'BlocoEntao': {
                'ENTAO': ['ENTAO', 'Comando', 'MaisComandos']
            },
            'Comando': {
                'ACAO': ['ACAO', 'Complemento']
            },
            'Complemento': {
                'ID_ENTIDADE': ['ID_ENTIDADE'],
                'STRING': ['STRING']
            },
            'MaisComandos': {
                'OP_LOGICO': ['OP_LOGICO', 'Comando', 'MaisComandos'],
                TOKEN_EOF: [] # Epsilon no final do arquivo
            }
        }

    def avancar_token(self):
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]

    def modo_panico(self, tokens_sincronizacao):
        self.erros.append(f"[ERRO SINTÁTICO] Modo Pânico ativado na linha {self.token_atual.linha}. Descartando tokens até encontrar: {tokens_sincronizacao}")
        
        while self.token_atual.tipo not in tokens_sincronizacao and self.token_atual.tipo != TOKEN_EOF:
            print(f"  -> Descartando token ignorado: {self.token_atual.valor}")
            self.avancar_token()

    def _log_iteracao(self, iteracao, acao_visual):
        pilha_visual = " ".join([simbolo for simbolo, _ in self.pilha])
        pilha_visual = ('...' + pilha_visual[-47:]) if len(pilha_visual) > 50 else pilha_visual
        
        entrada_visual = " ".join([t.tipo for t in self.tokens[self.posicao:]])
        entrada_visual = (entrada_visual[:27] + '...') if len(entrada_visual) > 30 else entrada_visual
        
        print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")

    def analisar(self):
        print("--- INICIANDO ANÁLISE SINTÁTICA ---")
        
        print(f"{'Iteração':<10} | {'Pilha':<50} | {'Entrada':<30} | {'Ação'}")
        print("-" * 120)
        
        iteracao = 1
        while len(self.pilha) > 0:
            # PASSO 1: Desempilha o elemento do topo e pega o token que o léxico está apontando agora.
            simbolo_topo, no_atual = self.pilha.pop()
            tipo_token = self.token_atual.tipo
            valor_token = self.token_atual.valor
            linha_atual = self.token_atual.linha
            
            # PASSO 2: CONDIÇÃO DE ACEITAÇÃO
            # Se o topo da pilha for o símbolo final '$', verificamos se a entrada também acabou ('EOF').
            if simbolo_topo == SIMBOLO_FIM_PILHA:
                if tipo_token == TOKEN_EOF:
                    self._log_iteracao(iteracao, "Aceitar")
                    return self.arvore
                else:
                    self.erros.append(f"[ERRO SINTÁTICO] Esperado fim de arquivo, mas encontrou '{valor_token}' na linha {linha_atual}.")
                    return None

            # PASSO 3: CONDIÇÃO DE MATCH (TERMINAIS)
            elif simbolo_topo in TERMINAIS: 
                if simbolo_topo == tipo_token:
                    self._log_iteracao(iteracao, f"Match '{valor_token}'")
                    # Se casou, salvamos o texto real (ex: "sensor.temperatura") no nó da árvore para usar na fase Semântica.
                    if no_atual:
                        no_atual.valor = valor_token
                    self.avancar_token()
                else:
                    self._log_iteracao(iteracao, "Erro")
                    self.erros.append(f"[ERRO SINTÁTICO] Esperado '{simbolo_topo}', mas encontrou '{valor_token}' na linha {linha_atual}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])
            
            # PASSO 4: CONDIÇÃO DE DERIVAÇÃO (NÃO-TERMINAIS)
            # Se o topo for uma regra (ex: BlocoQuando), consultamos a Tabela Preditiva cruzando a Regra com o Token Atual.
            else:
                if tipo_token in self.tabela.get(simbolo_topo, {}):
                    producao = self.tabela[simbolo_topo][tipo_token]
                    producao_str = " ".join(producao) if producao else "Epsilon"
                    self._log_iteracao(iteracao, f"{simbolo_topo} -> {producao_str}")
                    
                    # Cria nós na Árvore Sintática para os resultados dessa derivação.
                    novos_nos = [CSTNode(simbolo) for simbolo in producao]
                    if no_atual:
                        no_atual.filhos.extend(novos_nos)
                    
                    # Empilha os novos símbolos SEMPRE DE TRÁS PRA FRENTE (Reversed).
                    for simbolo, novo_no in reversed(list(zip(producao, novos_nos))):
                        self.pilha.append((simbolo, novo_no))
                else:
                    # Se a tabela não tiver uma transição mapeada, é um Erro de Sintaxe!
                    self._log_iteracao(iteracao, "Erro")
                    self.erros.append(f"[ERRO SINTÁTICO] Falha ao derivar '{simbolo_topo}' com token '{valor_token}' na linha {linha_atual}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])
                    
            iteracao += 1

        return self.arvore