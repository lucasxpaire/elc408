class CSTNode:
    """
    CSTNode (Concrete Syntax Tree Node) representa um "nó" ou "galho" na nossa árvore sintática.
    Detalhe Python: o método __init__ é o construtor da classe, chamado sempre que criamos um novo nó.
    O self é como se fosse o "this" do Java/C++, ele representa a própria instância do objeto.
    """
    def __init__(self, tipo):
        self.tipo = tipo # Ex: 'Programa', 'AUTOMACAO', 'ID_ENTIDADE'
        self.valor = None # Guarda a palavra em si (ex: "Ligar Luzes", "sensor.porta"). Fica vazio para regras.
        self.filhos = [] # Uma lista (Array) vazia que vai guardar outros nós CSTNode que estão "dentro" deste.
        
    def imprimir_arvore(self, nivel=0):
        """
        Função recursiva para desenhar a árvore no terminal usando indentação (espaços).
        Detalhe Python: nivel=0 significa que se você não passar um valor, ele assume 0 por padrão.
        """
        # Multiplicamos uma string vazia com espaços pelo nivel para dar o "recuo" da árvore
        indentacao = "  " * nivel
        
        # Montamos a linha do texto. Se tiver um valor, colocamos ": valor" no final
        texto = f"{indentacao}<{self.tipo}>"
        if self.valor:
            texto += f" : {self.valor}"
            
        resultado = texto + "\n"
        
        # Para cada filho dentro da lista de filhos, chamamos essa mesma função, mas com nivel + 1
        for filho in self.filhos:
            resultado += filho.imprimir_arvore(nivel + 1)
            
        return resultado
