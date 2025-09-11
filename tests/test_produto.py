import pytest

from nerdzone_cli.produto import Produto


def test_produto_criacao_valida():
    p = Produto(1, "Camiseta Python", "Algodão", 59.9, 10)
    assert p.id == 1
    assert p.nome == "Camiseta Python"
    assert p.preco == pytest.approx(59.9)
    assert p.estoque == 10


@pytest.mark.parametrize(
    "args,err",
    [
        ((1, " ", "d", 10.0, 1), ValueError),
        ((1, "Nome", "d", -1.0, 1), ValueError),
        ((1, "Nome", "d", 0.0, 1), ValueError),
        ((1, "Nome", "d", 10.0, -5), ValueError),
    ],
)
def test_produto_criacao_invalida(args, err):
    with pytest.raises(err):
        Produto(*args)


def test_atualizar_preco_valido_e_invalido():
    p = Produto(1, "Mouse", "", 100.0, 2)
    p.atualizar_preco(79.99)
    assert p.preco == pytest.approx(79.99)
    with pytest.raises(ValueError):
        p.atualizar_preco(0)
    with pytest.raises(ValueError):
        p.atualizar_preco(-10)


def test_adicionar_e_remover_estoque():
    p = Produto(1, "Teclado", "", 200.0, 5)
    p.adicionar_estoque(3)
    assert p.estoque == 8
    with pytest.raises(ValueError):
        p.adicionar_estoque(-1)
    with pytest.raises(ValueError):
        p.remover_estoque(-2)
    with pytest.raises(ValueError):
        p.remover_estoque(20)
    p.remover_estoque(3)
    assert p.estoque == 5


def test_row_roundtrip():
    p = Produto(42, "Caneca", "300ml", 35.5, 7)
    row = p.to_row()
    p2 = Produto.from_row({k: str(v) for k, v in row.items()})
    assert (p2.id, p2.nome, p2.descricao, p2.preco, p2.estoque) == (
        42,
        "Caneca",
        "300ml",
        35.5,
        7,
    )

