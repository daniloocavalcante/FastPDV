from banco import conectar


def adicionar_produto():
    print("\n======= CADASTRO DE PRODUTOS =======\n")

    nome = input("Nome do produto: ")
    preco = float(input("Preço: R$ "))
    estoque = int(input("Quantidade em estoque: "))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
        (nome, preco, estoque)
    )

    conexao.commit()
    conexao.close()

    print("""
Produto cadastrado com sucesso!
====================================
""")




def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    print("\n======= LISAGEM PRODUTOS =======")

    for produto in produtos:
        print(
            f"ID: {produto[0]} | Nome: {produto[1]} | "
            f"Preço: R$ {produto[2]:.2f} | Estoque: {produto[3]}"
        )    

    conexao.close()
    print("================================")
    
    



def excluir_produto():
    listar_produtos()

    print("\n======= EXCLUIR PRODUTOS =======")
    id_produto = input("Digite o ID do produto para excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))

    conexao.commit()
    conexao.close()

    print(f"Produto [ID: {id_produto}] removido com sucesso!")
    print("================================")