from database.banco import conectar


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


    print("\n=============== LISAGEM PRODUTOS ===============\n")
    print(f"{'ID':<5}{'PRECO':<10}{'ESTOQUE':<8}{'NOME'}")
    print("-" * 55)

    for produto in produtos:
        print(
            f"{produto[0]:<5}"
            f"R$ {produto[2]:<10}"
            f"{produto[3]:<8}"
            f"{produto[1]}"
        )

    print("================================================")

    conexao.close()
    
  

def excluir_produto():
    listar_produtos()

    print("\n======= EXCLUIR PRODUTOS =======")

    try:
        id_produto = int(input("Digite o ID do produto para excluir: "))
    except ValueError:
        print("Erro: o ID deve ser um número inteiro!")
        print("================================")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))

    if cursor.rowcount == 0:
        print(f"Produto [ID: {id_produto}] não encontrado!")
    else:
        conexao.commit()
        print(f"Produto [ID: {id_produto}] removido com sucesso!")

    conexao.close()

    print("================================")