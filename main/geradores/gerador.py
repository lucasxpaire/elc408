import random

class GeradorYAML:
    def __init__(self, arvore):
        self.arvore = arvore
        self.linhas_yaml = [] 

    def gerar(self):
        self.linhas_yaml = []
        id_aleatorio = random.randint(1000000000, 9999999999)
        self.linhas_yaml.append(f"- id: '{id_aleatorio}'")
        
        self.visitar_programa(self.arvore)
        
        yaml_final = "\n".join(self.linhas_yaml)
        print("Geração de Código concluída com SUCESSO!")
        return yaml_final

    def visitar_programa(self, no_programa):
        alias_node = None
        bloco_quando = None
        bloco_se = None
        bloco_entao = None
        
        for filho in no_programa.filhos:
            if filho.tipo == 'STRING':
                alias_node = filho
            elif filho.tipo == 'BlocoQuando':
                bloco_quando = filho
            elif filho.tipo == 'BlocoSe':
                bloco_se = filho
            elif filho.tipo == 'BlocoEntao':
                bloco_entao = filho

        if alias_node:
            self.linhas_yaml.append(f"  alias: {alias_node.valor}")
        else:
            self.linhas_yaml.append("  alias: \"Automação Homi\"")
            
        self.linhas_yaml.append("  description: \"Gerado automaticamente pelo Compilador Homi\"")
            
        self.linhas_yaml.append("  triggers:")
        if bloco_quando:
            self.visitar_quando(bloco_quando)
            
        # Verifica se o BlocoSe tem algum filho, senão é epsilon e não imprime condition
        if len(bloco_se.filhos) > 0:
            self.linhas_yaml.append("  conditions:")
            self.visitar_se(bloco_se)
            
        self.linhas_yaml.append("  actions:")
        if bloco_entao:
            self.visitar_entao(bloco_entao)
            
        self.linhas_yaml.append("  mode: single")

    def visitar_quando(self, no_quando):
        for filho in no_quando.filhos:
            if filho.tipo == 'RegraGatilho':
                tipo_node = filho.filhos[0]
                val_node = filho.filhos[1]
                
                if tipo_node.tipo == 'TIPO_GATILHO':
                    self.linhas_yaml.append("  - platform: time")
                    
                    tempo_node = val_node.filhos[0] # ComplementoGatilho guarda o TEMPO_EXATO ou TEMPO_UNIT
                    if tempo_node.tipo == 'TEMPO_EXATO':
                        horario = tempo_node.valor if len(tempo_node.valor) == 8 else tempo_node.valor + ":00"
                        self.linhas_yaml.append(f"    at: '{horario}'")
                    else:
                        # Fallback para o tempo_unit abstraido
                        self.linhas_yaml.append(f"    at: '{tempo_node.valor}'")

                elif tipo_node.tipo == 'ID_ENTIDADE':
                    # O ID_ENTIDADE foi o primeiro nó, o ESTADO é o terceiro nó (índice 2)
                    """
                    'RegraGatilho': {
                        'TIPO_GATILHO': ['TIPO_GATILHO', 'ComplementoGatilho'],
                        'ID_ENTIDADE': ['ID_ENTIDADE', 'OPERADOR', 'ESTADO']
                    }
                    """            
                    entidade = tipo_node.valor
                    estado_pt = filho.filhos[2].valor
                    
                    estado_en = 'on' if estado_pt in ['ligado', 'aberto', 'movimento'] else 'off'
                    self.linhas_yaml.append("  - platform: state")
                    self.linhas_yaml.append(f"    entity_id: {entidade}")
                    self.linhas_yaml.append(f"    to: '{estado_en}'")

    def visitar_se(self, no_se):
        condicoes = self.extrair_condicoes(no_se)
        for cond in condicoes:
            entidade = cond['entidade']
            estado_pt = cond['estado']
            
            estado_en = 'on' if estado_pt in ['ligado', 'aberto', 'movimento'] else 'off'
            
            self.linhas_yaml.append("  - condition: state")
            self.linhas_yaml.append(f"    entity_id: {entidade}")
            self.linhas_yaml.append(f"    state: '{estado_en}'")

    def extrair_condicoes(self, no):
        condicoes = []
        for filho in no.filhos:
            if filho.tipo == 'RegraCondicao':
                entidade = filho.filhos[0].valor
                estado = filho.filhos[2].valor
                condicoes.append({'entidade': entidade, 'estado': estado})
                
                mais_cond = filho.filhos[3]
                if len(mais_cond.filhos) > 0:
                    condicoes.extend(self.extrair_condicoes(mais_cond))
        return condicoes

    def visitar_entao(self, no_entao):
        comandos = self.extrair_comandos(no_entao)
        for cmd in comandos:
            acao = cmd['acao']
            alvo = cmd['alvo']
            
            if acao == 'ligar':
                dominio = alvo.split('.')[0]
                self.linhas_yaml.append(f"  - action: {dominio}.turn_on")
                self.linhas_yaml.append("    target:")
                self.linhas_yaml.append(f"      entity_id: {alvo}")
                
            elif acao == 'desligar':
                dominio = alvo.split('.')[0]
                self.linhas_yaml.append(f"  - action: {dominio}.turn_off")
                self.linhas_yaml.append("    target:")
                self.linhas_yaml.append(f"      entity_id: {alvo}")
                
            elif acao == 'alternar':
                dominio = alvo.split('.')[0]
                self.linhas_yaml.append(f"  - action: {dominio}.toggle")
                self.linhas_yaml.append("    target:")
                self.linhas_yaml.append(f"      entity_id: {alvo}")
                
            elif acao == 'notificar':
                self.linhas_yaml.append("  - action: notify.persistent_notification")
                self.linhas_yaml.append("    data:")
                self.linhas_yaml.append(f"      message: {alvo}")

    def extrair_comandos(self, no):
        comandos = []
        for filho in no.filhos:
            if filho.tipo == 'Comando':
                acao = filho.filhos[0].valor
                complemento_node = filho.filhos[1]
                alvo = complemento_node.filhos[0].valor
                comandos.append({'acao': acao, 'alvo': alvo})
            elif filho.tipo == 'MaisComandos':
                if len(filho.filhos) > 0:
                    comandos.extend(self.extrair_comandos(filho))
        return comandos
