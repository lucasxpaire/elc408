.PHONY: run test clean

run:
	@python main.py $(FILE)

test:
	@echo "=== Testando scripts exemplos validos ==="
	@python main.py exemplos/valido1.homi
	@echo ""
	@echo "=== Testando scripts exemplos invalidos (erro semantico) ==="
	@python main.py exemplos/invalido1.homi

clean:
	@del saida.yaml 2>nul
	@rmdir /s /q __pycache__ 2>nul
