from __future__ import annotations

import csv
import os
from typing import List, Optional

from .produto import Produto
from .logging_config import get_logger


CSV_FIELDS = ["id", "nome", "descricao", "preco", "estoque"]


class GerenciadorEstoque:
    def __init__(self, arquivo_csv: Optional[str] = None) -> None:
        self.produtos: List[Produto] = []
        self._next_id: int = 1
        self.arquivo_csv: Optional[str] = None
        self._logger = get_logger()
        if arquivo_csv:
            self.carregar_do_csv(arquivo_csv)

    def _atualiza_next_id(self) -> None:
        self._next_id = max((p.id for p in self.produtos), default=0) + 1

    def adicionar_produto(self, nome: str, descricao: str, preco: float, estoque: int) -> Produto:
        produto = Produto(self._next_id, nome, descricao, preco, estoque)
        self.produtos.append(produto)
        self._next_id += 1
        self._auto_salvar()
        try:
            self._logger.info(
                "Produto adicionado: '%s' (ID: %s) com %s unidades em estoque.",
                produto.nome,
                produto.id,
                produto.estoque,
            )
        except Exception:
            pass
        return produto

    def buscar_produto_por_id(self, id_produto: int) -> Optional[Produto]:
        try:
            id_produto = int(id_produto)
        except (TypeError, ValueError):
            return None
        for p in self.produtos:
            if p.id == id_produto:
                return p
        return None

    def listar_produtos(self) -> List[Produto]:
        return list(self.produtos)

    def atualizar_estoque(self, id_produto: int, quantidade: int) -> bool:
        produto = self.buscar_produto_por_id(id_produto)
        if not produto:
            return False
        estoque_antes = produto.estoque
        if quantidade >= 0:
            produto.adicionar_estoque(quantidade)
        else:
            produto.remover_estoque(-quantidade)
        self._auto_salvar()
        try:
            self._logger.info(
                "Estoque atualizado: '%s' (ID: %s) %s -> %s (delta %+d)",
                produto.nome,
                produto.id,
                estoque_antes,
                produto.estoque,
                quantidade,
            )
        except Exception:
            pass
        return True

    def remover_produto(self, id_produto: int) -> bool:
        produto = self.buscar_produto_por_id(id_produto)
        if not produto:
            return False
        self.produtos.remove(produto)
        self._auto_salvar()
        try:
            self._logger.info("Produto removido: '%s' (ID: %s)", produto.nome, produto.id)
        except Exception:
            pass
        return True

    def atualizar_preco(self, id_produto: int, novo_preco: float) -> bool:
        produto = self.buscar_produto_por_id(id_produto)
        if not produto:
            return False
        preco_antigo = produto.preco
        produto.atualizar_preco(novo_preco)
        self._auto_salvar()
        try:
            self._logger.info(
                "Preço atualizado: '%s' (ID: %s) de %.2f para %.2f",
                produto.nome,
                produto.id,
                preco_antigo,
                produto.preco,
            )
        except Exception:
            pass
        return True

    def salvar_em_csv(self, nome_arquivo: Optional[str] = None) -> None:
        arquivo = nome_arquivo or self.arquivo_csv
        if not arquivo:
            raise ValueError("Arquivo CSV não especificado.")
        pasta = os.path.dirname(os.path.abspath(arquivo))
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for p in self.produtos:
                writer.writerow(p.to_row())
        self.arquivo_csv = arquivo
        try:
            self._logger.info("Catálogo salvo em '%s' (%d produtos)", arquivo, len(self.produtos))
        except Exception:
            pass

    def carregar_do_csv(self, nome_arquivo: str) -> None:
        self.produtos.clear()
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        self.produtos.append(Produto.from_row(row))
                    except Exception:
                        # Ignora linhas inválidas
                        continue
            try:
                self._logger.info("Catálogo carregado de '%s' (%d produtos)", nome_arquivo, len(self.produtos))
            except Exception:
                pass
        else:
            try:
                self._logger.info("Arquivo CSV não encontrado; iniciando catálogo vazio em '%s'", nome_arquivo)
            except Exception:
                pass
        self.arquivo_csv = nome_arquivo
        self._atualiza_next_id()

    def _auto_salvar(self) -> None:
        if self.arquivo_csv:
            self.salvar_em_csv(self.arquivo_csv)
