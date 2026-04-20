import json

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from pdf_report import generar_pdf
from scanner import escanear
from analyzer import analizar
from database import conectar, crear_tablas, crear_admin, guardar_log
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "securescan_secret_key"


crear_tablas()
crear_admin()


# ==========================================
# LOGIN
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE username=?",
            (username,)
        )

        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario[2], password):

            session["usuario"] = usuario[1]
            session["rol"] = usuario[3]

            guardar_log(usuario[1], "Inició sesión")

            return redirect(url_for("index"))

    return render_template("login.html")


# ==========================================
# LOGOUT
# ==========================================
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


# ==========================================
# PANEL ADMIN
# ==========================================
@app.route("/admin", methods=["GET", "POST"])
def panel_admin():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO usuarios (username,password,rol) VALUES (?,?,?)",
            (username, password_hash, rol)
        )

        conn.commit()

        guardar_log(session["usuario"], f"Creó usuario {username}")

    cursor.execute("SELECT id, username, rol FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("""
        SELECT usuario, accion, fecha
        FROM logs
        ORDER BY fecha DESC
        LIMIT 20
    """)
    logs = cursor.fetchall()

    conn.close()

    return render_template("admin.html", usuarios=usuarios, logs=logs)


# ==========================================
# ELIMINAR USUARIO
# ==========================================
@app.route("/eliminar_usuario/<int:id>")
def eliminar_usuario(id):

    if session["rol"] != "admin":
        return "Acceso denegado"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()

    guardar_log(session["usuario"], f"Eliminó usuario {id}")

    return redirect(url_for("panel_admin"))


# ==========================================
# DASHBOARD
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()

    riesgos = None
    recomendaciones = None
    alto = medio = bajo = 0
    pdf = None

    if request.method == "POST":

        if session["rol"] not in ["admin", "analista"]:
            return "No tienes permiso"

        ip = request.form["ip"]

        scan = escanear(ip)
        riesgos, recomendaciones = analizar(scan)

        pdf = generar_pdf(ip, riesgos, recomendaciones)

        cursor.execute(
            "INSERT INTO escaneos (ip, riesgos) VALUES (?,?)",
            (ip, json.dumps(riesgos))
        )

        conn.commit()

        guardar_log(session["usuario"], f"Escaneó {ip}")

        alto = sum(1 for r in riesgos if "🔴" in r)
        medio = sum(1 for r in riesgos if "🟡" in r or "🟠" in r)
        bajo = sum(1 for r in riesgos if "🟢" in r)

    cursor.execute("SELECT mensaje FROM alertas ORDER BY fecha DESC LIMIT 10")
    alertas = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT ip, fecha FROM escaneos ORDER BY fecha DESC LIMIT 5")
    historial = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        riesgos=riesgos,
        recomendaciones=recomendaciones,
        alto=alto,
        medio=medio,
        bajo=bajo,
        pdf=pdf,
        alertas=alertas,
        historial=historial
    )


# ==========================================
# API
# ==========================================

@app.route("/api/dashboard")
def api_dashboard():
    conn = conectar()
    cursor = conn.cursor()

    # Total IPs únicas escaneadas
    cursor.execute("""
        SELECT COUNT(DISTINCT ip) as total
        FROM escaneos
    """)
    hosts = cursor.fetchone()["total"] or 0

    # Riesgos críticos
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM escaneos
        WHERE riesgos LIKE '%🔴%'
    """)
    riesgos = cursor.fetchone()["total"] or 0

    # Promedio score
    cursor.execute("""
        SELECT AVG(score) as promedio
        FROM escaneos
    """)
    fila = cursor.fetchone()
    score = int(fila["promedio"]) if fila["promedio"] else 0

    # Eventos hoy
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM logs
        WHERE DATE(fecha)=DATE('now','localtime')
    """)
    eventos = cursor.fetchone()["total"] or 0

    # Historial y alertas
    cursor.execute("SELECT ip, fecha FROM escaneos ORDER BY fecha DESC LIMIT 5")
    historial = cursor.fetchall()

    cursor.execute("SELECT mensaje FROM alertas ORDER BY fecha DESC LIMIT 5")
    alertas = [row[0] for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "riesgos_criticos": riesgos,
        "hosts": hosts,
        "score": score,
        "eventos": eventos,
        "historial": historial,
        "alertas": alertas
    })


# ==========================================
# SCAN
# ==========================================

@app.route("/api/scan", methods=["POST"])
def api_scan():

    data = request.get_json()
    ip = data["ip"]

    resultado = escanear(ip)

    puertos = []

    for linea in resultado.split("\n"):
        if "/tcp" in linea and "open" in linea:
            puerto = linea.split("/")[0].strip()
            puertos.append(puerto)

    riesgos, recomendaciones = analizar(resultado)

    score = 100

    for r in riesgos:
        if "🔴" in r:
            score -= 15
        elif "🟡" in r or "🟠" in r:
            score -= 8
        else:
            score -= 3

    if score < 0:
        score = 0

    # GUARDAR EN SQLITE
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO escaneos (ip, puertos, riesgos, score, usuario)
        VALUES (?, ?, ?, ?, ?)
    """, (
        ip,
        ",".join(puertos),
        " | ".join(riesgos),
        score,
        "admin"
    ))

    cursor.execute("""
        INSERT INTO logs (usuario, accion)
        VALUES (?, ?)
    """, (
        "admin",
        f"Escaneo ejecutado a {ip}"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "ip": ip,
        "riesgos": riesgos,
        "recomendaciones": recomendaciones,
        "score": score,
        "puertos": puertos
    })


@app.route("/api/history")
def api_history():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip, score, puertos, fecha
        FROM escaneos
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    historial = []

    for row in rows:
        historial.append({
            "ip": row["ip"],
            "score": row["score"],
            "puertos": row["puertos"],
            "fecha": row["fecha"]
        })

    return jsonify(historial)


if __name__ == "__main__":
    app.run(debug=True)