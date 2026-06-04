import sys
import os

# Adiciona o diretório 'main' no escopo para facilitar os imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 1. Importa as fases do compilador
from analisadores.lexico import analisador_lexico
from analisadores.sintatico import AnalisadorSintatico
from analisadores.semantico import AnalisadorSemantico
from geradores.gerador import GeradorYAML

def main():
    print("========================================")
    print("      COMPILADOR HOMI - INICIADO        ")
    print("========================================\n")

    # DETALHE PYTHON: sys.argv é uma lista que pega o que você digitou no terminal.
    # sys.argv[0] é sempre o nome do script ('main.py'). sys.argv[1] será o arquivo passado ('meucodigo.homi').
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
        if not os.path.exists(caminho_arquivo):
            print(f"[ERRO] O arquivo '{caminho_arquivo}' não foi encontrado.")
            return
            
        print(f"Lendo código do arquivo: {caminho_arquivo}")
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
    else:
        print("Aviso: Nenhum arquivo passado por parâmetro. Rodando código de teste embutido...\n")
        codigo_fonte = """
        AUTOMACAO "Ligar Luzes da Sala"
        #teste comentario
        QUANDO horario 18:00
        SE light.sala_estar estiver desligado
        ENTAO ligar light.sala_estar
        E notificar "Luzes ligadas!"
        """

    # --- FASE 1: ANÁLISE LÉXICA ---
    print("\n[FASE 1] A executar o Analisador Léxico...")
    tokens_gerados, erro_lexico = analisador_lexico(codigo_fonte)
    print(f"-> {len(tokens_gerados)} tokens válidos extraídos.\n")

    if erro_lexico:
        print("RESULTADO LÉXICO: Falha! Encontrados caracteres inválidos no código.")
        print("A compilação foi interrompida.")
        return

    # --- FASE 2: ANÁLISE SINTÁTICA ---
    print("[FASE 2] A executar o Analisador Sintático...")
    parser = AnalisadorSintatico(tokens_gerados)
    sucesso_sintatico, arvore = parser.analisar()

    if sucesso_sintatico:
        print(" RESULTADO SINTÁTICO: Sucesso! Código Homi bem estruturado.\n")
        
        # --- FASE 3: ANÁLISE SEMÂNTICA ---
        print("[FASE 3] A executar o Analisador Semântico...")
        analisador_semantico = AnalisadorSemantico(arvore)
        sucesso_semantico = analisador_semantico.analisar()
        
        if sucesso_semantico:
            print(" RESULTADO SEMÂNTICO: Tudo 100% coerente!\n")
            
            # --- FASE 4: GERAÇÃO DE CÓDIGO (YAML) ---
            print("[FASE 4] A executar o Gerador YAML...")
            gerador = GeradorYAML(arvore)
            codigo_final = gerador.gerar()
            
            print("\n========================================")
            print("CÓDIGO YAML GERADO COM SUCESSO:")
            print("========================================\n")
            print(codigo_final)
            print("\n========================================\n")
            
            # Salvar no arquivo
            caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "saida.yaml")
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(codigo_final)
            print(f"-> O arquivo final 'saida.yaml' foi salvo com sucesso em main/outputs/!")
            
        else:
            print("\nRESULTADO SEMÂNTICO: Foram encontrados absurdos lógicos nas instruções.")
    else:
        print("\nRESULTADO SINTÁTICO: Falha! Encontrados erros de sintaxe.")
        print("A compilação foi interrompida.")

if __name__ == "__main__":
    main()