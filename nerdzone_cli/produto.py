from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        if not self.nome:
            raise ValueError("Nome do produto não pode ser vazio.")
        try:
            self.preco = float(self.preco)
        except (TypeError, ValueError) as exc:
            raise ValueError("Preço inválido.") from exc
        if self.preco <= 0:
            raise ValueError("Preço deve ser positivo.")
        try:
            self.estoque = int(self.estoque)
        except (TypeError, ValueError) as exc:
            raise ValueError("Estoque inválido.") from exc
        if self.estoque < 0:
            raise ValueError("Estoque não pode ser negativo.")

    def atualizar_preco(self, novo_preco: float) -> None:
        try:
            novo_preco = float(novo_preco)
        except (TypeError, ValueError) as exc:
            raise ValueError("Preço inválido.") from exc
        if novo_preco <= 0:
            raise ValueError("Preço deve ser positivo.")
        self.preco = round(novo_preco, 2)

    def adicionar_estoque(self, quantidade: int) -> None:
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError) as exc:
            raise ValueError("Quantidade inválida.") from exc
        if quantidade < 0:
            raise ValueError("Quantidade para adicionar deve ser não negativa.")
        self.estoque += quantidade

    def remover_estoque(self, quantidade: int) -> None:
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError) as exc:
            raise ValueError("Quantidade inválida.") from exc
        if quantidade < 0:
            raise ValueError("Quantidade para remover deve ser não negativa.")
        if quantidade > self.estoque:
            raise ValueError("Estoque insuficiente.")
        self.estoque -= quantidade

    def to_row(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": f"{self.preco:.2f}",
            "estoque": self.estoque,
        }

    @staticmethod
    def from_row(row: dict[str, str]) -> "Produto":
        return Produto(
            id=int(row.get("id", 0)),
            nome=row.get("nome", "").strip(),
            descricao=row.get("descricao", ""),
            preco=float(row.get("preco", 0)),
            estoque=int(row.get("estoque", 0)),
        )

    def __str__(self) -> str:
        return f"#{self.id} | {self.nome} | R$ {self.preco:.2f} | Estoque: {self.estoque}"

