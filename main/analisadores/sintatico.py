from estruturas.arvore import CSTNode

TOKEN_EOF = 'EOF'
SIMBOLO_FIM_PILHA = '$'

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens + [(TOKEN_EOF, SIMBOLO_FIM_PILHA, tokens[-1][2] if tokens else 1)]
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
        """
        Recuperação de Erros (Requisito C): 
        Descarta tokens até encontrar um ponto seguro para continuar a análise.
        """
        self.erros.append(f"[ERRO SINTÁTICO] Modo Pânico ativado na linha {self.token_atual[2]}. Descartando tokens até encontrar: {tokens_sincronizacao}")
        
        while self.token_atual[0] not in tokens_sincronizacao and self.token_atual[0] != TOKEN_EOF:
            print(f"  -> Descartando token ignorado: {self.token_atual[1]}")
            self.avancar_token()

    def analisar(self):
        print("--- INICIANDO ANÁLISE SINTÁTICA ---")
        
        print(f"{'Iteração':<10} | {'Pilha':<50} | {'Entrada':<30} | {'Ação'}")
        print("-" * 120)
        
        iteracao = 1
        
        while len(self.pilha) > 0:
            pilha_visual = " ".join([simbolo for simbolo, _ in self.pilha])
            pilha_visual = ('...' + pilha_visual[-47:]) if len(pilha_visual) > 50 else pilha_visual
            
            entrada_visual = " ".join([t[0] for t in self.tokens[self.posicao:]])
            entrada_visual = (entrada_visual[:27] + '...') if len(entrada_visual) > 30 else entrada_visual
            
            topo, no_atual = self.pilha.pop()
            tipo_token = self.token_atual[0]
            valor_token = self.token_atual[1]
            linha_atual = self.token_atual[2]
            
            acao_visual = ""

            if topo == SIMBOLO_FIM_PILHA:
                if tipo_token == TOKEN_EOF:
                    acao_visual = "Aceitar"
                    print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")
                    return self.arvore
                else:
                    self.erros.append(f"[ERRO SINTÁTICO] Esperado fim de arquivo, mas encontrou '{valor_token}' na linha {linha_atual}.")
                    return None

            elif topo.isupper() or topo == 'STRING': 
                if topo == tipo_token:
                    acao_visual = f"Match '{valor_token}'"
                    print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")
                    
                    if no_atual:
                        no_atual.valor = valor_token
                    self.avancar_token()
                else:
                    acao_visual = "Erro"
                    print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")
                    self.erros.append(f"[ERRO SINTÁTICO] Esperado '{topo}', mas encontrou '{valor_token}' na linha {linha_atual}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])
            
            else:
                if tipo_token in self.tabela.get(topo, {}):
                    producao = self.tabela[topo][tipo_token]
                    producao_str = " ".join(producao) if producao else "Epsilon"
                    acao_visual = f"{topo} -> {producao_str}"
                    print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")
                    
                    novos_nos = [CSTNode(simbolo) for simbolo in producao]
                    
                    if no_atual:
                        no_atual.filhos.extend(novos_nos)
                    
                    for simbolo, novo_no in reversed(list(zip(producao, novos_nos))):
                        self.pilha.append((simbolo, novo_no))
                else:
                    acao_visual = "Erro"
                    print(f"{iteracao:<10} | {pilha_visual:<50} | {entrada_visual:<30} | {acao_visual}")
                    self.erros.append(f"[ERRO SINTÁTICO] Falha ao derivar '{topo}' com token '{valor_token}' na linha {linha_atual}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])
                    
            iteracao += 1

        return self.arvore