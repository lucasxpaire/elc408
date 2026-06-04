from estruturas.arvore import CSTNode

TOKEN_EOF = 'EOF'
SIMBOLO_FIM_PILHA = '$'

class AnalisadorSintatico:
    def __init__(self, tokens):
        # Adicionamos um token de Fim de Arquivo ($) para indicar o término
        self.tokens = tokens + [(TOKEN_EOF, SIMBOLO_FIM_PILHA, tokens[-1][2] if tokens else 1)]
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao]
        
        # Criamos o Nó Raiz da nossa Árvore (O ponto de partida)
        self.arvore = CSTNode('Programa')
        
        # A Pilha inicia com o Fim de Arquivo e o Não-Terminal inicial.
        # Agora estamos guardando Tuplas na pilha: (NomeDaRegra, NóDaArvore).
        # Isso serve para sabermos em qual galho da árvore devemos pendurar as próximas palavras.
        self.pilha = [(SIMBOLO_FIM_PILHA, None), ('Programa', self.arvore)]
        
        # Variável para rastrear se o arquivo teve algum erro de sintaxe durante a varredura
        self.teve_erro = False
        
        # Tabela Preditiva LL(1) (Mapeamento das Regras)
        # Formato: tabela[Nao_Terminal][Token_Lido] = [Regras a empilhar]
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
                'VERBO_ACAO': ['VERBO_ACAO', 'Complemento']
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
        print(f"[ERRO SINTÁTICO] Modo Pânico ativado na linha {self.token_atual[2]}.")
        print(f"Descartando tokens até encontrar: {tokens_sincronizacao}")
        
        self.teve_erro = True
        
        while self.token_atual[0] not in tokens_sincronizacao and self.token_atual[0] != TOKEN_EOF:
            print(f"  -> Descartando token ignorado: {self.token_atual[1]}")
            self.avancar_token()

    def analisar(self):
        print("--- INICIANDO ANÁLISE SINTÁTICA ---")
        
        while len(self.pilha) > 0:
            # DETALHE PYTHON: "Desempacotamento de Tupla". O pop() devolve a tupla e já separamos em 2 variáveis.
            topo, no_atual = self.pilha.pop()
            tipo_token = self.token_atual[0]
            valor_token = self.token_atual[1]
            linha_atual = self.token_atual[2]

            if topo == SIMBOLO_FIM_PILHA:
                if tipo_token == TOKEN_EOF:
                    if not self.teve_erro:
                        print("Análise Sintática concluída com SUCESSO!")
                    # Agora retornamos se houve erro e a Árvore preenchida!
                    return not self.teve_erro, self.arvore
                else:
                    print(f"[ERRO] Esperado fim de arquivo, mas encontrou '{valor_token}' na linha {linha_atual}.")
                    return False, None

            # Se o topo for um Terminal
            elif topo.isupper() or topo == 'STRING': 
                if topo == tipo_token:
                    print(f"  [Match Terminal] {topo} consumiu '{valor_token}'")
                    # MAGIA DA ÁRVORE: Quando dá match, guardamos a palavra real no "galho" que estava esperando por ela.
                    if no_atual:
                        no_atual.valor = valor_token
                    self.avancar_token()
                else:
                    print(f"[ERRO SINTÁTICO] Esperado '{topo}', mas encontrou '{valor_token}' na linha {linha_atual}.")
                    # Ativa Modo Pânico: Tenta pular para o próximo bloco lógico seguro
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])
            
            # Se o topo for um Não-Terminal (consulta a Tabela LL1)
            else:
                if tipo_token in self.tabela.get(topo, {}):
                    producao = self.tabela[topo][tipo_token]
                    print(f"[Derivação] {topo} -> {producao}")
                    
                    # MAGIA DA ÁRVORE: Criamos novos "galhinhos" menores para cada símbolo derivado
                    novos_nos = [CSTNode(simbolo) for simbolo in producao]
                    
                    # Conectamos esses novos nós como 'filhos' do nó em que estamos no momento
                    if no_atual:
                        no_atual.filhos.extend(novos_nos)
                    
                    # Empilha de trás para frente, juntando o símbolo com seu respectivo nó
                    # DETALHE PYTHON: zip(A, B) junta duas listas em uma lista de tuplas [(a1,b1), (a2,b2)...]
                    for simbolo, novo_no in reversed(list(zip(producao, novos_nos))):
                        self.pilha.append((simbolo, novo_no))
                else:
                    print(f"[ERRO SINTÁTICO] Falha ao derivar '{topo}' com token '{valor_token}' na linha {linha_atual}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', TOKEN_EOF])

        return not self.teve_erro, self.arvore