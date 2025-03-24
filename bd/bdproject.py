import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")

conn.execute('''
CREATE TABLE clientes (
    email TEXT PRIMARY KEY,
    cpf INTEGER,
    telefone TEXT,
    data_aniversario TEXT
)
''')

conn.execute('''
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_email TEXT,
    produto TEXT,
    FOREIGN KEY (cliente_email) REFERENCES clientes(email)
)
''')

clientes = [
    ("samara@email.com", 12345678900, "123456789", "1990-01-01"),
    ("luffy@email.com", 98765432100, "987654321", "1985-05-15"),
    ("zoro@email.com", 54321678900, "567890123", "1992-07-20")
]

pedidos = [
    ("samara@email.com", "O ladrão de raios"),
    ("luffy@email.com", "O mar de monstros"),
    ("zoro@email.com", "O último olimpiano")
]

conn.executemany("INSERT INTO clientes (email, cpf, telefone, data_aniversario) VALUES (?, ?, ?, ?)", clientes)
conn.executemany("INSERT INTO pedidos (cliente_email, produto) VALUES (?, ?)", pedidos)

query_inner = """
SELECT clientes.email, clientes.cpf, clientes.telefone, pedidos.produto
FROM clientes
INNER JOIN pedidos ON clientes.email = pedidos.cliente_email
"""
inner_join_df = pd.read_sql(query_inner, conn)
print("INNER JOIN:")
print(inner_join_df)

query_left = """
SELECT clientes.email, clientes.cpf, clientes.telefone, pedidos.produto
FROM clientes
LEFT JOIN pedidos ON clientes.email = pedidos.cliente_email
"""
left_join_df = pd.read_sql(query_left, conn)
print("\nLEFT JOIN:")
print(left_join_df)

conn.close()