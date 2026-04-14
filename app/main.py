import json
from flask import Flask, render_template, request
from scanner import escanear
from analyzer import analizar
from flask import jsonify
from database import conectar
from database import crear_tablas

crear_tablas()


app = Flask(__name__)

@app.route("/alertas")
def obtener_alertas():
    import json
    try:
        with open("app/alerts.json", "r") as f:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT mensaje FROM alertas ORDER BY fecha DESC LIMIT 10")
            alertas = [row[0] for row in cursor.fetchall()]
            

            cursor.execute("SELECT ip, fecha FROM escaneos ORDER BY fecha DESC LIMIT 5")
            historial = cursor.fetchall()


            conn.close()


    except:
        alertas = []

    return jsonify(alertas)

@app.route("/", methods=["GET", "POST"])
def index():
 if request.method == "POST":
    ip = request.form["ip"]

    scan = escanear(ip)
    riesgos, recomendaciones = analizar(scan)

    # Guardar escaneo en la base de datos
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO escaneos (ip, riesgos) VALUES (?, ?)",
        (ip, json.dumps(riesgos))
    )

    conn.commit()
    conn.close()

    # Contar riesgos por nivel
    alto = sum(1 for r in riesgos if "🔴" in r)
    medio = sum(1 for r in riesgos if "🟡" in r or "🟠" in r)
    bajo = sum(1 for r in riesgos if "🟢" in r)

        
    try:
            with open("app/alerts.json", "r") as f:
                alertas = json.load(f)
    except:
            alertas = []

    return render_template(
            "index.html",
            riesgos=riesgos,
            recomendaciones=recomendaciones,
            alto=alto,
            medio=medio,
            bajo=bajo
        )

    # GET (cuando abres la página por primera vez)
    return render_template(
        "index.html",
        riesgos=None,
        recomendaciones=None,
        alto=0,
        medio=0,
        bajo=0
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)