import re

TOKEN_REGEX = [
    ('AUTOMACAO', r'\bAUTOMACAO\b'),
    ('QUANDO',    r'\bQUANDO\b'),
    ('SE',        r'\bSE\b'),
    ('ENTAO',     r'\bENTAO\b'),
    ('OP_LOGICO', r'\b(E|OU|NAO)\b'),                      
    ('VERBO_ACAO',r'\b(ligar|desligar|alternar|notificar)\b'),
    ('ESTADO',    r'\b(ligado|desligado|aberto|fechado|movimento|ocioso)\b'),
    ('OPERADOR',  r'\b(for|estiver)\b'),
    ('TIPO_GATILHO', r'\b(horario|tempo)\b'),
    ('TEMPO_EXATO',r'\b\d{2}:\d{2}\b'),                    
    ('TEMPO_UNIT', r'\b\d+(s|m|min|h|hs)\b'),              
    ('ID_ENTIDADE',r'\b[a-z_]+\.[a-z0-9_]+\b'),            
    ('STRING',    r'".*?"'),                               
    ('ESPACO',    r'[ \t]+'),                              
    ('NOVA_LINHA',r'\n'),                                  
    ('COMENTARIO',r'#.*'),                                 
    ('ERRO',      r'.')                                    
]

class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens_encontrados = []
        self.linha_atual = 1
        self.teve_erro = False

    def analisar(self):
        regex_combinada = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_REGEX)
        
        for match in re.finditer(regex_combinada, self.codigo_fonte):
            tipo_token = match.lastgroup
            valor_token = match.group(tipo_token)

            if tipo_token == 'NOVA_LINHA':
                self.linha_atual += 1
            elif tipo_token == 'ESPACO' or tipo_token == 'COMENTARIO':
                continue 
            elif tipo_token == 'ERRO':
                print(f"[ERRO LÉXICO] Caractere ou palavra inválida '{valor_token}' na linha {self.linha_atual}")
                self.teve_erro = True
            else:
                self.tokens_encontrados.append((tipo_token, valor_token, self.linha_atual))
                
        return self.tokens_encontrados, self.teve_erro
