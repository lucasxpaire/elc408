class NodoCST:
    """
    Representa um nó da Árvore de Sintaxe Concreta (CST).
    Armazena o símbolo da gramática, seu valor literal (se for um terminal) e seus nós filhos.
    """
    def __init__(self, tipo):
        self.tipo = tipo
        self.valor = None
        self.filhos = []
        
    def imprimir_arvore(self, nivel=0):
        """
        Gera uma representação textual e hierárquica da árvore para depuração.
        """
        indentacao = "  " * nivel
        texto = f"{indentacao}<{self.tipo}>"
        
        if self.valor:
            texto += f" : {self.valor}"
            
        resultado = texto + "\n"
        
        for filho in self.filhos:
            resultado += filho.imprimir_arvore(nivel + 1)
            
        return resultado
