from werkzeug.security import generate_password_hash
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        rol TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        accion TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def crear_admin():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = [
        ("admin", "1234", "admin"),
        ("analista", "1234", "analista"),
        ("auditor", "1234", "auditor")
    ]

    for username, password, rol in usuarios:
        hash_pw = generate_password_hash(password)

        cursor.execute("""
        INSERT OR IGNORE INTO usuarios (username, password, rol)
        VALUES (?, ?, ?)
        """, (username, hash_pw, rol))

    conn.commit()
    conn.close()

def guardar_log(usuario, accion):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (usuario, accion) VALUES (?, ?)",
        (usuario, accion)
    )

    conn.commit()
    conn.close()