.PHONY: run test-lexico test-sintatico test-semantico

run:
	@echo "Executando o compilador com o script de teste padrão..."
	@python main/main.py main/inputs/test_padrao.homi

test-lexico:
	@echo "Testando tratamento de Erro Léxico..."
	@python main/main.py main/inputs/test_erro_lexico.homi

test-sintatico:
	@echo "Testando tratamento de Erro Sintático (Modo Pânico)..."
	@python main/main.py main/inputs/test_erro_sintatico.homi

test-semantico:
	@echo "Testando tratamento de Erro Semântico..."
	@python main/main.py main/inputs/test_erro_semantico_2.homi
