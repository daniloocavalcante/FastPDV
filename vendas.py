from database.banco import conectar
from clientes import listar_clientes
from produtos import listar_produtos


def realizar_venda():
    conexao = conectar()
    cursor = conexao.cursor()

    cliente_id = int(input("ID do cliente: "))

    cursor.execute(
        "SELECT id FROM clientes WHERE id = ?",
        (cliente_id,)
    )

    if not cursor.fetchone():
        print("Cliente não encontrado.")
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO vendas (cliente_id)
        VALUES (?)
    """, (cliente_id,))

    venda_id = cursor.lastrowid

    total_venda = 0

    while True:
        print("\nDigite 0 para finalizar a venda.")

        produto_id = int(input("ID do produto: "))

        if produto_id == 0:
            break

        cursor.execute("""
            SELECT nome, preco, estoque
            FROM produtos
            WHERE id = ?
        """, (produto_id,))

        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado.")
            continue

        nome, preco, estoque = produto

        print(f"Produto: {nome}")
        print(f"Preço: R$ {preco:.2f}")
        print(f"Estoque: {estoque}")

        quantidade = int(input("Quantidade: "))

        if quantidade <= 0:
            print("Quantidade inválida.")
            continue

        if quantidade > estoque:
            print("Estoque insuficiente.")
            continue

        subtotal = preco * quantidade

        cursor.execute("""
            INSERT INTO itens_venda
            (venda_id, produto_id, quantidade, subtotal)
            VALUES (?, ?, ?, ?)
        """, (
            venda_id,
            produto_id,
            quantidade,
            subtotal
        ))

        cursor.execute("""
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE id = ?
        """, (
            quantidade,
            produto_id
        ))

        total_venda += subtotal

        print(
            f"Item adicionado. "
            f"Subtotal: R$ {subtotal:.2f}"
        )

    cursor.execute("""
        UPDATE vendas
        SET total = ?
        WHERE id = ?
    """, (
        total_venda,
        venda_id
    ))

    conexao.commit()
    conexao.close()

    print("\nVenda finalizada!")
    print(f"ID da venda: {venda_id}")
    print(f"Total: R$ {total_venda:.2f}")


def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            vendas.id,
            clientes.nome,
            vendas.total,
            vendas.data_venda
        FROM vendas
        JOIN clientes
            ON vendas.cliente_id = clientes.id
        ORDER BY vendas.id
    """)

    vendas = cursor.fetchall()

    print("\n===================== VENDAS =====================")

    if not vendas:
        print("Nenhuma venda cadastrada.")
    else:
        print(f"{'ID':<5}{'CLIENTE':<25}{'TOTAL':<12}{'DATA'}")
        print("-" * 55)

        for venda in vendas:
            print(
                f"{venda[0]:<5}"
                f"{venda[1]:<25}"
                f"R$ {venda[2]:<9.2f}"
                f"{venda[3]}"
            )

    print("==================================================")

    conexao.close()

    opcao = input("\nDeseja detalhar uma venda? (s/n): ").lower()

    if opcao == "s":
        detalhar_venda()


def detalhar_venda():
    id_venda = input("Digite o ID da venda: ")

    try:
        id_venda = int(id_venda)
    except ValueError:
        print("ID inválido.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            vendas.id,
            clientes.nome,
            vendas.total,
            vendas.data_venda
        FROM vendas
        JOIN clientes
            ON vendas.cliente_id = clientes.id
        WHERE vendas.id = ?
    """, (id_venda,))

    venda = cursor.fetchone()

    if not venda:
        print("Venda não encontrada.")
        conexao.close()
        return

    print(f"\n========== VENDA #{venda[0]} ==========")
    print(f"Cliente: {venda[1]}")
    print(f"Data: {venda[3]}")
    print()

    print(f"{'PRODUTO':<25}{'QTD':<8}{'SUBTOTAL'}")
    print("-" * 45)

    cursor.execute("""
        SELECT
            produtos.nome,
            itens_venda.quantidade,
            itens_venda.subtotal
        FROM itens_venda
        JOIN produtos
            ON itens_venda.produto_id = produtos.id
        WHERE itens_venda.venda_id = ?
    """, (id_venda,))

    itens = cursor.fetchall()

    for item in itens:
        print(
            f"{item[0]:<25}"
            f"{item[1]:<8}"
            f"R$ {item[2]:.2f}"
        )

    print("-" * 45)
    print(f"TOTAL: R$ {venda[2]:.2f}")
    print("=" * 45)

    conexao.close()