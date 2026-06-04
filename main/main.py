import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analisadores.lexico import AnalisadorLexico
from analisadores.sintatico import AnalisadorSintatico
from analisadores.semantico import AnalisadorSemantico
from geradores.gerador import GeradorYAML

def carregar_codigo_fonte():
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
        if not os.path.exists(caminho_arquivo):
            print(f"[ERRO] O arquivo '{caminho_arquivo}' não foi encontrado.")
            return None
            
        print(f"Lendo código do arquivo: {caminho_arquivo}")
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print("Aviso: Nenhum arquivo passado por parâmetro. Rodando código de teste embutido...\n")
        return """
        AUTOMACAO "Ligar Luzes da Sala"
        #teste comentario
        QUANDO horario 18:00
        SE light.sala_estar estiver desligado
        ENTAO ligar light.sala_estar
        E notificar "Luzes ligadas!"
        """

def salvar_arquivo_saida(codigo_final):
    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "saida.yaml")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(codigo_final)
    print(f"-> O arquivo final 'saida.yaml' foi salvo com sucesso em main/outputs/!")

def main():
    print("--- Compilador Homi ---")
    codigo_fonte = carregar_codigo_fonte()
    if codigo_fonte is None:
        return

    print("\n[FASE 1] Analisador Léxico")
    lexer = AnalisadorLexico(codigo_fonte)
    tokens_gerados, erro_lexico = lexer.analisar()
    print(f"-> {len(tokens_gerados)} tokens válidos extraídos.")
    if erro_lexico:
        print("[AVISO] Erros léxicos encontrados. Continuando análise para encontrar mais erros...")

    print("\n[FASE 2] Analisador Sintático")
    parser = AnalisadorSintatico(tokens_gerados)
    sucesso_sintatico, arvore = parser.analisar()
    
    if sucesso_sintatico:
        print("[FASE 3] Analisador Semântico")
        analisador_semantico = AnalisadorSemantico(arvore)
        sucesso_semantico = analisador_semantico.analisar()
        if sucesso_semantico:
            if erro_lexico:
                print("\n[FALHA GERAL] O código possui erros léxicos. Geração de YAML cancelada.")
                return
            print("\n[FASE 4] Gerador YAML")
            gerador = GeradorYAML(arvore)
            codigo_final = gerador.gerar()
            salvar_arquivo_saida(codigo_final)
        else:
            print("[ERRO] Falha Semântica.")
    else:
        print("[ERRO] Falha Sintática.")

if __name__ == "__main__":
    main()