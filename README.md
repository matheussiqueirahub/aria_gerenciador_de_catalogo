[![CI](https://github.com/matheussiqueirahub/aria_gerenciador_de_catalogo/actions/workflows/tests.yml/badge.svg)](https://github.com/matheussiqueirahub/aria_gerenciador_de_catalogo/actions/workflows/tests.yml) [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#)

Aria – Gerenciador de Catálogo (CLI)

Ferramenta de linha de comando para gerenciar o catálogo de e‑commerce (produtos geek) com Python, OOP, persistência em CSV e logging.

Principais recursos
- Produtos: id sequencial, nome, descrição, preço (>0) e estoque (>=0).
- Operações: adicionar, listar, buscar por ID, atualizar preço, atualizar estoque (entrada/saída), remover.
- Persistência: salva e carrega automaticamente de `dados/produtos.csv`.
- Logs: registra operações em `logs/estoque.log` com rotação.

Estrutura
- `main.py`: CLI interativa (menu 1–7), carrega/salva automaticamente.
- `nerdzone_cli/produto.py`: classe `Produto` + validações e helpers CSV.
- `nerdzone_cli/gerenciador.py`: `GerenciadorEstoque` (negócio + salvar/carregar CSV).
- `nerdzone_cli/logging_config.py`: configuração de logging (arquivo rotativo).
- `tests/`: testes unitários com `pytest`.

Demo (GIF)
- Pré-gerado: `docs/demo.cast` (gravação em formato Asciinema v2).
- Gerar GIF a partir do `.cast` (requer o agregador `agg`/`asciinema-agg` instalado):
  - Comando: `agg -i docs/demo.cast -o docs/demo.gif --theme dracula --speed 1.1 --cols 80 --rows 24`
- Depois, o GIF pode ser visualizado/embutido aqui:

![Demo da CLI](docs/demo.gif)

Requisitos
- Python 3.8+ (testado em 3.13)
- Opcional (para testes): `pytest`

Como executar
- No terminal, execute: `python main.py`
- O catálogo é salvo em `dados/produtos.csv` (criado na primeira alteração).

Menu da CLI:
1. Adicionar Produto
2. Listar Todos os Produtos
3. Atualizar Preço de um Produto
4. Atualizar Estoque de um Produto (positivo = entrada, negativo = saída)
5. Buscar Produto por ID
6. Remover Produto
7. Sair

Dicas:
- O preço aceita vírgula ou ponto (ex.: `49,90` ou `49.90`).
- A remoção de estoque é impedida se resultar em valor negativo.

Persistência (CSV)
- Caminho padrão: `dados/produtos.csv`.
- Colunas: `id,nome,descricao,preco,estoque`.
- IDs são sequenciais e recalculados como `max(id) + 1` ao carregar.
- Para usar outro CSV, você pode ajustar `ARQUIVO_PADRAO` em `main.py:9`.

Logs
- Arquivo: `logs/estoque.log` (UTF‑8). Nível: INFO.
- Rotação: até ~1MB por arquivo, mantém 3 backups.
- Registra: adicionar produto, atualizar preço/estoque, remover, salvar/carregar CSV e início/fim da aplicação.

Testes
- Instalar dependência (se necessário): `python -m pip install -U pytest`
- Rodar: `python -m pytest -q`

Próximos passos (sugestões)
- Validação avançada: regras adicionais (nome mínimo, limites de preço/estoque, etc.).
- Categorias: classe `Categoria` e listagem por categoria.
- API REST: expor o gerenciador via Flask/FastAPI (`GET/POST /produtos`).
- Empacotamento: transformar em pacote/console_script para instalação via pip.

