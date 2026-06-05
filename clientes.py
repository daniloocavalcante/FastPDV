from database.banco import conectar


def adicionar_cliente():

    print("\n======= CADASTRO DE CLIENTES =======\n")
    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
        (nome, telefone)
    )

    conexao.commit()
    conexao.close()
    print("""
Cliente cadastrado com sucesso!
====================================
""")


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n=================== CLIENTES ===================\n")
    print(f"{'ID':<5}{'NOME':<20}{'TELEFONE':<15}{'EMAIL'}")
    print("-" * 55)

    for cliente in clientes:
        print(
            f"{cliente[0]:<5}"
            f"{cliente[1]:<20}"
            f"{cliente[2]:<15}"
            f"{cliente[3]}"
        )

    print("================================================")

    conexao.close()



def excluir_cliente():
    listar_clientes()

    print("\n======= EXCLUIR CLIENTES =======")

    try:
        id_cliente = int(input("Digite o ID do cliente para excluir: "))
    except ValueError:
        print("Erro: o ID deve ser um número inteiro!")
        print("================================")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))

    if cursor.rowcount == 0:
        print(f"Cliente [ID: {id_cliente}] não encontrado!")
    else:
        conexao.commit()
        print(f"Cliente [ID: {id_cliente}] removido com sucesso!")

    conexao.close()

    print("================================")