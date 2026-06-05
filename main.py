from database.banco import conectar
import os


from database.banco import (
    criar_tabelas,
    resetar_banco,
    popular_banco
)

from clientes import (
    adicionar_cliente,
    listar_clientes,
    excluir_cliente
)

from produtos import (
    adicionar_produto,
    listar_produtos,
    excluir_produto
)

from vendas import (
    realizar_venda,
    listar_vendas
)


def menu_clientes():
    while True:

        limpar_tela()

        print("""
======== GERENCIAR CLIENTES ========
1 - Adicionar Cliente
2 - Listar Clientes
3 - Excluir Cliente
0 - Voltar
====================================
""")        
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        acoes = {
            "1": adicionar_cliente,
            "2": listar_clientes,
            "3": excluir_cliente,
        }

        if acoes.get(opcao):
            acoes.get(opcao)()
            input("\nPressione ENTER para voltar...")

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")


   


def menu_produtos():
    while True:

        limpar_tela()

        print("""
======== GERENCIAR PRODUTOS ========
1 - Adicionar Produto
2 - Listar Produtos
3 - Excluir Produto
0 - Voltar
====================================
""")

        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            break

        acoes = {
            "1": adicionar_produto,
            "2": listar_produtos,
            "3": excluir_produto,
        }

        if acoes.get(opcao):
            acoes.get(opcao)()
            input("\nPressione ENTER para voltar...")

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")



def menu_vendas():
    while True:
        limpar_tela()

        print("""
============ VENDAS ============
1 - Realizar Venda
2 - Listar Vendas
0 - Voltar
================================
""")

        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            break
        

        acoes = {
            "1": realizar_venda,
            "2": listar_vendas,
        }

        if acoes.get(opcao):
            acoes.get(opcao)()
            input("\nPressione ENTER para voltar...")

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")


def configs():
    while True:
        limpar_tela()

        print("""
=========== CONFIGURAÇÕES ===========
1 - Criar Banco de Dados
2 - Popular Banco de Dados
3 - Resetar Banco de Dados
0 - Voltar
=====================================
""")

        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            break        

        acoes = {
            "1": criar_tabelas,
            "2": popular_banco,
            "3": resetar_banco,
        }

        if acoes.get(opcao):
            acoes.get(opcao)()
            input("\nPressione ENTER para voltar...")

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")


def main():
    criar_tabelas()

    while True:
        limpar_tela()

        print("""
===================================
            SISTEMA PDV
===================================
1 - Clientes
2 - Produtos
3 - Vendas
4 - Configurações
0 - Sair
===================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        acoes = {
            "1": menu_clientes,
            "2": menu_produtos,
            "3": menu_vendas,
            "4": configs,
        }

        if acoes.get(opcao):
            acoes.get(opcao)()

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")




def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()