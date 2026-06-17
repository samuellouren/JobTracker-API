import sqlite3

def conectar():
    conn = sqlite3.connect("vagas.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 empresa TEXT NOT NULL,
                 cargo TEXT NOT NULL,
                 status TEXT NOT NULL,
                 data TEXT NOT NULL
    )
""")
    conn.commit()
    conn.close()