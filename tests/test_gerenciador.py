from __future__ import annotations

import csv
from pathlib import Path

import pytest

from nerdzone_cli.gerenciador import GerenciadorEstoque


def ler_csv_cabecalho(caminho: Path):
    with caminho.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def test_adicionar_e_persistir_produto(tmp_path: Path):
    csv_path = tmp_path / "catalogo.csv"
    g = GerenciadorEstoque(str(csv_path))
    p = g.adicionar_produto("Action Figure", "Star Wars", 199.9, 3)
    assert p.id == 1
    assert csv_path.exists() and csv_path.stat().st_size > 0

    # Recarregar
    g2 = GerenciadorEstoque(str(csv_path))
    p_loaded = g2.buscar_produto_por_id(1)
    assert p_loaded is not None
    assert p_loaded.nome == "Action Figure"
    assert g2._next_id == 2  # próximo id sequencial


def test_atualizar_estoque_e_preco_persiste(tmp_path: Path):
    csv_path = tmp_path / "catalogo.csv"
    g = GerenciadorEstoque(str(csv_path))
    p = g.adicionar_produto("Copo", "Marvel", 29.9, 10)

    assert g.atualizar_estoque(p.id, 5)
    assert g.buscar_produto_por_id(p.id).estoque == 15
    assert g.atualizar_estoque(p.id, -4)
    assert g.buscar_produto_por_id(p.id).estoque == 11

    assert g.atualizar_preco(p.id, 24.9)
    assert g.buscar_produto_por_id(p.id).preco == pytest.approx(24.9)

    # Recarregar e verificar persistência
    g2 = GerenciadorEstoque(str(csv_path))
    p2 = g2.buscar_produto_por_id(p.id)
    assert p2 is not None
    assert p2.estoque == 11
    assert p2.preco == pytest.approx(24.9)


def test_remover_produto(tmp_path: Path):
    csv_path = tmp_path / "catalogo.csv"
    g = GerenciadorEstoque(str(csv_path))
    p = g.adicionar_produto("Poster", "Ghibli", 19.9, 2)
    assert g.remover_produto(p.id)
    assert g.buscar_produto_por_id(p.id) is None

    g2 = GerenciadorEstoque(str(csv_path))
    assert g2.buscar_produto_por_id(p.id) is None


def test_buscar_invalido_e_listar_copia(tmp_path: Path):
    csv_path = tmp_path / "catalogo.csv"
    g = GerenciadorEstoque(str(csv_path))
    g.adicionar_produto("Livro", "Sci-Fi", 49.9, 7)
    assert g.buscar_produto_por_id("abc") is None  # id inválido

    lst = g.listar_produtos()
    assert len(lst) == 1
    lst.clear()
    # limpeza na cópia não altera o gerenciador
    assert len(g.listar_produtos()) == 1

