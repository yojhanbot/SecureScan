from flask import Flask, render_template, request
from scanner import escanear
from analyzer import analizar

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        ip = request.form["ip"].strip()
        scan = escanear(ip)
        riesgos, recomendaciones = analizar(scan)

        alto = sum(1 for r in riesgos if "🔴" in r)
        medio = sum(1 for r in riesgos if "🟡" in r or "🟠" in r)
        bajo = sum(1 for r in riesgos if "🟢" in r)

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