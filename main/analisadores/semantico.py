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
        """
        Verifica se a condição solicitada faz sentido para a entidade.
        Exemplo: Um 'sensor' pode estar 'quente', mas não 'ligado'.
        """
        # Garante que a regra possui filhos e que o primeiro é o ID da Entidade.
        if not no_regra.filhos or no_regra.filhos[0].tipo != 'ID_ENTIDADE':
            return
            
        no_entidade = no_regra.filhos[0]
        no_estado = no_regra.filhos[2]
                
        if no_entidade and no_estado:
            entidade_id = no_entidade.valor
            estado_desejado = no_estado.valor
            
            # Passo 1: Verifica se a entidade existe na Tabela de Símbolos
            if entidade_id not in self.tabela_simbolos:
                self.reportar_erro(f"Entidade '{entidade_id}' não declarada na Tabela de Símbolos.")
                return
                
            # Passo 2: Descobre o domínio (tipo) da entidade
            dominio = self.tabela_simbolos[entidade_id]
            
            # Passo 3: Verifica se o domínio suporta o estado solicitado
            if estado_desejado not in self.estados_permitidos.get(dominio, []):
                self.reportar_erro(f"Incompatibilidade de Tipo: A entidade '{entidade_id}' ({dominio}) não suporta o estado '{estado_desejado}'.")

    def validar_comando(self, no_comando):
        """
        Verifica se a ação solicitada é aplicável ao tipo da entidade.
        Exemplo: Pode-se 'ligar' uma 'lâmpada', mas não um 'sensor_num'.
        """
        # Garante que o comando tenha a estrutura esperada (Ação + Complemento)
        if len(no_comando.filhos) != 2:
            return
            
        no_acao = no_comando.filhos[0]
        no_complemento = no_comando.filhos[1]

        acao_desejada = no_acao.valor
        
        # O verbo 'notificar' independe de entidade física, então já é válido por padrão
        if acao_desejada == 'notificar':
            return 

        # Se a ação alvejar uma entidade física (ex: ligar switch.tv)
        if no_complemento.filhos and no_complemento.filhos[0].tipo == 'ID_ENTIDADE':
            no_id_entidade = no_complemento.filhos[0]
            entidade_id = no_id_entidade.valor
            
            # Passo 1: Verifica se a entidade existe na Tabela de Símbolos
            if entidade_id not in self.tabela_simbolos:
                self.reportar_erro(f"Entidade '{entidade_id}' não declarada na Tabela de Símbolos.")
                return
                
            # Passo 2: Descobre o domínio (tipo) da entidade
            dominio = self.tabela_simbolos[entidade_id]
            
            # Passo 3: Verifica se o domínio suporta a ação solicitada
            if acao_desejada not in self.acoes_permitidas.get(dominio, []):
                self.reportar_erro(f"Incompatibilidade de Tipo: Não é possível '{acao_desejada}' a entidade '{entidade_id}' (Domínio: {dominio}).")
