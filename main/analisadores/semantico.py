class AnalisadorSemantico:
    """
    O Analisador Semântico verifica as regras lógicas e a consistência externa (mundo real).
    Ele garante que as instruções façam sentido para o Home Assistant.
    """
    def __init__(self, arvore):
        self.arvore = arvore
        self.erros = [] 
        
        self.tabela_simbolos = {
            'light.sala_estar': 'light',
            'light.quarto': 'light',
            'switch.tv': 'switch',
            'switch.ilha_interruptor_1': 'switch',
            'binary_sensor.porta': 'binary_sensor',
            'sensor.temperatura': 'sensor_num',
            'sensor.temperature_living_room': 'sensor_num'
        }
        
        self.acoes_permitidas = {
            'light': ['ligar', 'desligar', 'alternar'],
            'switch': ['ligar', 'desligar', 'alternar'],
            'binary_sensor': [],
            'sensor_num': []
        }
        
        self.estados_permitidos = {
            'light': ['ligado', 'desligado'],
            'switch': ['ligado', 'desligado'],
            'binary_sensor': ['aberto', 'fechado', 'movimento', 'ocioso'],
            'sensor_num': [] 
        }

    def analisar(self):
        self.percorrer_arvore(self.arvore)
        return len(self.erros) == 0

    def percorrer_arvore(self, no):
        """
        Navegação Baseada na Árvore Sintática (AST)
        """
        if no.tipo == 'Comando':
            self.validar_comando(no)
        elif no.tipo == 'RegraCondicao' or no.tipo == 'RegraGatilho':
            self.validar_estado(no)
            
        for filho in no.filhos:
            self.percorrer_arvore(filho)

    def reportar_erro(self, mensagem):
        erro = f"[ERRO SEMÂNTICO] {mensagem}"
        self.erros.append(erro)

    def validar_estado(self, no_regra):
        """ Valida se uma entidade pode estar em um determinado estado """
        entidade_node = None
        estado_node = None
        
        for filho in no_regra.filhos:
            if filho.tipo == 'ID_ENTIDADE':
                entidade_node = filho
            elif filho.tipo == 'ESTADO':
                estado_node = filho
                
        if entidade_node and estado_node:
            entidade = entidade_node.valor
            estado = estado_node.valor
            
            if entidade not in self.tabela_simbolos:
                self.reportar_erro(f"Entidade '{entidade}' não declarada na Tabela de Símbolos.")
                return
                
            dominio = self.tabela_simbolos[entidade]
            
            if estado not in self.estados_permitidos.get(dominio, []):
                self.reportar_erro(f"Incompatibilidade de Tipo: A entidade '{entidade}' ({dominio}) não suporta o estado '{estado}'.")

    def validar_comando(self, no_comando):
        verbo_node = None
        complemento_node = None
        
        for filho in no_comando.filhos:
            if filho.tipo == 'VERBO_ACAO':
                verbo_node = filho
            elif filho.tipo == 'Complemento':
                complemento_node = filho
                
        if not verbo_node or not complemento_node:
            return

        verbo = verbo_node.valor
        if verbo == 'notificar':
            return 

        id_entidade_node = None
        for filho in complemento_node.filhos:
            if filho.tipo == 'ID_ENTIDADE':
                id_entidade_node = filho
                break
                
        if id_entidade_node:
            entidade = id_entidade_node.valor
            
            if entidade not in self.tabela_simbolos:
                self.reportar_erro(f"Entidade '{entidade}' não declarada na Tabela de Símbolos.")
                return
                
            dominio = self.tabela_simbolos[entidade]
            
            if verbo not in self.acoes_permitidas.get(dominio, []):
                self.reportar_erro(f"Incompatibilidade de Tipo: Não é possível '{verbo}' a entidade '{entidade}' (Domínio: {dominio}).")
