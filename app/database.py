from werkzeug.security import generate_password_hash
import sqlite3

DB_PATH = "app/securescan.db"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL,
        creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Escaneos reales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escaneos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        puertos TEXT,
        riesgos TEXT,
        score INTEGER DEFAULT 0,
        usuario TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Alertas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT DEFAULT 'general',
        mensaje TEXT NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        accion TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Hosts monitoreados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hosts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT UNIQUE,
        estado TEXT DEFAULT 'online',
        ultimo_check DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Índices
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_escaneos_fecha ON escaneos(fecha)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_fecha ON logs(fecha)")

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

    cursor.execute("""
    INSERT INTO logs (usuario, accion)
    VALUES (?, ?)
    """, (usuario, accion))

    conn.commit()
    conn.close()