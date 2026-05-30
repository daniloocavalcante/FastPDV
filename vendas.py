from banco import conectar
from clientes import listar_clientes
from produtos import listar_produtos



def realizar_venda():
    print("\n========= REALIZAR VENDA =========")

    listar_clientes()
    cliente_id = int(input("\nID do cliente: "))

    listar_produtos()
    produto_id = int(input("\nID do produto: "))

    quantidade = int(input("Quantidade: "))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT preco, estoque FROM produtos WHERE id = ?",
        (produto_id,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        print("Produto não encontrado!")
        conexao.close()
        return

    preco, estoque = resultado

    if quantidade > estoque:
        print("\nEstoque insuficiente!")
        conexao.close()
        return

    total = preco * quantidade

    novo_estoque = estoque - quantidade

    cursor.execute(
        "UPDATE produtos SET estoque = ? WHERE id = ?",
        (novo_estoque, produto_id)
    )

    cursor.execute(
        "INSERT INTO vendas (cliente_id, produto_id, quantidade, total) VALUES (?, ?, ?, ?)",
        (cliente_id, produto_id, quantidade, total)
    )

    conexao.commit()
    conexao.close()
    print("\n================================")

    print(f"Venda realizada com sucesso!")
    print(f"TOTAL DA COMPRA: R$ {total:.2f}")
    print("================================")




def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
    SELECT
        vendas.id,
        clientes.nome,
        produtos.nome,
        vendas.quantidade,
        vendas.total
    FROM vendas
    JOIN clientes ON vendas.cliente_id = clientes.id
    JOIN produtos ON vendas.produto_id = produtos.id
    ''')

    vendas = cursor.fetchall()

    print("\n========= LISTAR VENDAS =========")

    for venda in vendas:
        print(
            f"ID: {venda[0]} | Cliente: {venda[1]} | Total: {venda[4]:.2f}")
    conexao.close()
    print("=================================")