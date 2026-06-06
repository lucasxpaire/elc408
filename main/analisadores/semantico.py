class AnalisadorSemantico:
    
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
            'sensor_num': ['quente', 'frio', 'normal'] 
        }

    def analisar(self):
        self.percorrer_arvore(self.arvore)
        return len(self.erros) == 0

    def percorrer_arvore(self, no):
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
        if not no_regra.filhos or no_regra.filhos[0].tipo != 'ID_ENTIDADE':
            return
            
        entidade_node = no_regra.filhos[0]
        estado_node = no_regra.filhos[2]
                
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
        if len(no_comando.filhos) != 2:
            return
            
        acao_node = no_comando.filhos[0]
        complemento_node = no_comando.filhos[1]

        acao = acao_node.valor
        if acao == 'notificar':
            return 

        if complemento_node.filhos and complemento_node.filhos[0].tipo == 'ID_ENTIDADE':
            id_entidade_node = complemento_node.filhos[0]
            entidade = id_entidade_node.valor
            
            if entidade not in self.tabela_simbolos:
                self.reportar_erro(f"Entidade '{entidade}' não declarada na Tabela de Símbolos.")
                return
                
            dominio = self.tabela_simbolos[entidade]
            
            if acao not in self.acoes_permitidas.get(dominio, []):
                self.reportar_erro(f"Incompatibilidade de Tipo: Não é possível '{acao}' a entidade '{entidade}' (Domínio: {dominio}).")
