import sqlite3

def conectar():

    return sqlite3.connect("airside.db")

def criar_tabelas():

    conn = conectar()

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    data TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS projetos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    vazao REAL,
    data TEXT
    )
    """)

    conn.commit()

    conn.close()
