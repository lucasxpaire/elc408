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
    else:
        print("Aviso: Nenhum arquivo passado por parâmetro. Rodando código de teste padrão...\n")
        caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs", "test_padrao.homi")
        
    if not os.path.exists(caminho_arquivo):
        print(f"[ERRO] O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)
        
    print(f"Lendo código do arquivo: {caminho_arquivo}")
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return f.read()

def salvar_arquivo_saida(codigo_final, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(codigo_final)

def main():
    print("--- Compilador Homi ---")
    codigo_fonte = carregar_codigo_fonte()
    
    print("\n[FASE 1] Analisador Léxico")
    analisador_lexico = AnalisadorLexico(codigo_fonte)
    tokens_gerados = analisador_lexico.analisar()
    print(f"-> {len(tokens_gerados)} tokens válidos extraídos.")

    print("\n[FASE 2] Analisador Sintático")
    analisador_sintatico = AnalisadorSintatico(tokens_gerados)
    arvore = analisador_sintatico.analisar()
    
    print("\n[FASE 3] Analisador Semântico")
    analisador_semantico = AnalisadorSemantico(arvore)
    analisador_semantico.analisar()
        
    todos_erros = analisador_lexico.erros + analisador_sintatico.erros + analisador_semantico.erros
    if len(todos_erros) > 0:
        print("\n========================================")
        print("          RELATÓRIO DE ERROS            ")
        print("========================================")
        for erro in todos_erros:
            print(erro)
        print("========================================")
        print("-> A compilação foi abortada e o YAML não será gerado.")
        return

    print("\n[FASE 4] Gerador YAML")
    gerador = GeradorYAML(arvore)
    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "saida.yaml")
    codigo_final = gerador.gerar()
    salvar_arquivo_saida(codigo_final, caminho_saida)
    print(f"-> Arquivo YAML gerado com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    main()