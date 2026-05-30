from banco import conectar


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

    print("\n======= LISAGEM CLIENTES =======")

    for cliente in clientes:
        print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Telefone: {cliente[2]}")

    conexao.close()    
    print("================================")




def excluir_cliente():
    listar_clientes()
    
    print("\n======= EXCLUIR CLIENTES =======")
    id_cliente = input("Digite o ID do cliente para excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))

    conexao.commit()
    conexao.close()

    print(f"Cliente [ID: {id_cliente}] removido com sucesso!")
    print("================================")