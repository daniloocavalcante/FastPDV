import sqlite3
import random


def conectar():
    conexao = sqlite3.connect("fast-pdv.db")
    return conexao

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total REAL DEFAULT 0,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (venda_id) REFERENCES vendas(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    conexao.commit()
    conexao.close()


def resetar_banco():

    print("\n============= RESETAR BANCO ==============\n")

    confirmacao = input(
        "Tem certeza que deseja resetar o banco de dados? Todos os dados serão perdidos. (s/n): "
    ).lower()

    if confirmacao != "s":
        print("Operação cancelada.")
        return
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DROP TABLE IF EXISTS itens_venda")
    cursor.execute("DROP TABLE IF EXISTS vendas")
    cursor.execute("DROP TABLE IF EXISTS produtos")
    cursor.execute("DROP TABLE IF EXISTS clientes")

    conexao.commit()
    conexao.close()

    criar_tabelas()

    print("""
Banco de dados resetado com sucesso!
==========================================
""")



def popular_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    print("Populando: Clientes...")

    clientes = [
        ("Ana Silva", "2190000-0001", "ana@email.com"),
        ("Bruno Souza", "5190000-0002", "bruno@email.com"),
        ("Carlos Lima", "5390000-0003", "carlos@email.com"),
        ("Daniela Rocha", "6190000-0004", "daniela@email.com"),
        ("Eduardo Santos", "7190000-0005", "eduardo@email.com"),
        ("Fernanda Alves", "2190000-0006", "fernanda@email.com"),
        ("Gabriel Costa", "2190000-0007", "gabriel@email.com"),
        ("Helena Martins", "2290000-0008", "helena@email.com"),
        ("Igor Oliveira", "8590000-0009", "igor@email.com"),
        ("Juliana Pereira", "8190000-0010", "juliana@email.com")
    ]

    cursor.executemany(
        "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
        clientes
    )

    print("Populando: Produtos...")

    produtos = [
        ("Arroz 5kg", 29.90, 50),
        ("Feijão 1kg", 8.99, 80),
        ("Macarrão", 4.50, 100),
        ("Açúcar 1kg", 5.20, 60),
        ("Sal 1kg", 2.50, 70),
        ("Café 500g", 18.90, 40),
        ("Leite 1L", 5.80, 120),
        ("Refrigerante 2L", 9.99, 90),
        ("Biscoito", 3.75, 150),
        ("Chocolate", 6.90, 100),
        ("Sabão em Pó", 14.90, 35),
        ("Detergente", 2.99, 90),
        ("Papel Higiênico", 19.90, 45),
        ("Shampoo", 17.50, 40),
        ("Condicionador", 18.50, 35),
        ("Creme Dental", 7.99, 80),
        ("Escova Dental", 5.99, 60),
        ("Água Mineral", 2.00, 200),
        ("Suco 1L", 7.50, 70),
        ("Óleo de Soja", 8.90, 50)
    ]

    cursor.executemany(
        "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
        produtos
    )

    print("Populando: Vendas...")

    for _ in range(30):
        cliente_id = random.randint(1, 10)

        # Cria a venda
        cursor.execute("""
            INSERT INTO vendas (cliente_id)
            VALUES (?)
        """, (cliente_id,))

        venda_id = cursor.lastrowid
        total_venda = 0

        # Cada venda terá entre 1 e 5 itens
        qtd_itens = random.randint(1, 5)

        produtos_utilizados = set()

        for _ in range(qtd_itens):
            produto_id = random.randint(1, 20)

            while produto_id in produtos_utilizados:
                produto_id = random.randint(1, 20)

            produtos_utilizados.add(produto_id)

            quantidade = random.randint(1, 5)

            cursor.execute("""
                SELECT preco, estoque
                FROM produtos
                WHERE id = ?
            """, (produto_id,))

            resultado = cursor.fetchone()

            if not resultado:
                continue

            preco, estoque = resultado

            # Evita estoque negativo
            if estoque <= 0:
                continue

            if quantidade > estoque:
                quantidade = estoque

            subtotal = round(preco * quantidade, 2)

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

            # Atualiza estoque
            cursor.execute("""
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ?
            """, (
                quantidade,
                produto_id
            ))

            total_venda += subtotal

        # Atualiza total da venda
        cursor.execute("""
            UPDATE vendas
            SET total = ?
            WHERE id = ?
        """, (
            round(total_venda, 2),
            venda_id
        ))

    conexao.commit()
    conexao.close()

    print("\nBanco populado com sucesso!")
    print("==========================================")