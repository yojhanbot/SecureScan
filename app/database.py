import sqlite3

def conectar():
    return sqlite3.connect("app/securescan.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escaneos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        riesgos TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mensaje TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()