from __future__ import annotations

import os
from typing import Optional

from nerdzone_cli.gerenciador import GerenciadorEstoque
from nerdzone_cli.logging_config import configure_logging, get_logger


ARQUIVO_PADRAO = os.path.join("dados", "produtos.csv")


def input_nao_vazio(msg: str) -> str:
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("Entrada vazia. Tente novamente.")


def input_float_positivo(msg: str) -> float:
    while True:
        valor = input(msg).replace(",", ".").strip()
        try:
            num = float(valor)
            if num > 0:
                return num
            print("Informe um número maior que zero.")
        except ValueError:
            print("Valor inválido. Tente novamente.")


def input_int(msg: str) -> int:
    while True:
        valor = input(msg).strip()
        try:
            return int(valor)
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def input_int_nao_negativo(msg: str) -> int:
    while True:
        n = input_int(msg)
        if n >= 0:
            return n
        print("Informe um inteiro não negativo.")


def mostrar_menu() -> None:
    print("\n=== NerdZone | Gerenciador de Estoque ===")
    print("1. Adicionar Produto")
    print("2. Listar Todos os Produtos")
    print("3. Atualizar Preço de um Produto")
    print("4. Atualizar Estoque de um Produto")
    print("5. Buscar Produto por ID")
    print("6. Remover Produto")
    print("7. Sair")


def imprimir_lista(ger: GerenciadorEstoque) -> None:
    produtos = ger.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    print("\nID  | Nome                          | Preço    | Estoque | Descrição")
    print("-" * 80)
    for p in produtos:
        print(f"{p.id:>3} | {p.nome[:28]:<28} | R$ {p.preco:>7.2f} | {p.estoque:>7} | {p.descricao}")


def main(arquivo_csv: Optional[str] = None) -> None:
    arquivo = arquivo_csv or ARQUIVO_PADRAO
    configure_logging()
    logger = get_logger()
    try:
        logger.info("Aplicação iniciada")
    except Exception:
        pass
    ger = GerenciadorEstoque(arquivo)

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção (1-7): ").strip()

        if opcao == "1":
            print("\n-- Adicionar Produto --")
            nome = input_nao_vazio("Nome: ")
            descricao = input("Descrição (opcional): ").strip()
            preco = input_float_positivo("Preço (ex: 49.90): ")
            estoque = input_int_nao_negativo("Estoque inicial: ")
            try:
                produto = ger.adicionar_produto(nome, descricao, preco, estoque)
                print(f"Produto adicionado com sucesso: ID {produto.id}.")
            except Exception as e:
                print(f"Erro ao adicionar produto: {e}")

        elif opcao == "2":
            print("\n-- Lista de Produtos --")
            imprimir_lista(ger)

        elif opcao == "3":
            print("\n-- Atualizar Preço --")
            id_produto = input_int("ID do produto: ")
            novo_preco = input_float_positivo("Novo preço: ")
            try:
                ok = ger.atualizar_preco(id_produto, novo_preco)
                if ok:
                    print("Preço atualizado e salvo.")
                else:
                    print("Produto não encontrado.")
            except Exception as e:
                print(f"Erro ao atualizar preço: {e}")

        elif opcao == "4":
            print("\n-- Atualizar Estoque --")
            id_produto = input_int("ID do produto: ")
            print("Use valores positivos para entrada e negativos para saída.")
            quantidade = input_int("Quantidade (+/-): ")
            try:
                ok = ger.atualizar_estoque(id_produto, quantidade)
                if ok:
                    print("Estoque atualizado e salvo.")
                else:
                    print("Produto não encontrado.")
            except Exception as e:
                print(f"Erro ao atualizar estoque: {e}")

        elif opcao == "5":
            print("\n-- Buscar Produto --")
            id_produto = input_int("ID do produto: ")
            p = ger.buscar_produto_por_id(id_produto)
            if p:
                print("Encontrado:")
                print(f"ID: {p.id}")
                print(f"Nome: {p.nome}")
                print(f"Descrição: {p.descricao}")
                print(f"Preço: R$ {p.preco:.2f}")
                print(f"Estoque: {p.estoque}")
            else:
                print("Produto não encontrado.")

        elif opcao == "6":
            print("\n-- Remover Produto --")
            id_produto = input_int("ID do produto: ")
            ok = ger.remover_produto(id_produto)
            if ok:
                print("Produto removido e alterações salvas.")
            else:
                print("Produto não encontrado.")

        elif opcao == "7":
            print("Saindo... Até logo!")
            try:
                logger.info("Aplicação finalizada")
            except Exception:
                pass
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
