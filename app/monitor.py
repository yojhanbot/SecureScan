import time
import json
from scanner import escanear
from email_alert import enviar_alerta  
from database import conectar

def monitorear(ip):

    estado_anterior = set()

    while True:
        resultado = escanear(ip)

        puertos = set()

        for linea in resultado.split("\n"):
            if "/tcp" in linea and "open" in linea:
                puerto = linea.split("/")[0]
                puertos.add(puerto)

        nuevos = puertos - estado_anterior

        # Si hay puertos nuevos, enviar alerta
        if nuevos and estado_anterior:
            mensaje = f"🚨 Puertos nuevos detectados: {nuevos}"
            print(mensaje)
            enviar_alerta(mensaje)

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
            "INSERT INTO alertas (mensaje) VALUES (?)",
            (mensaje,)
)

            conn.commit()
            conn.close()

            # Guardar alerta en JSON
    try:
        with open("app/alerts.json", "r") as f:
            alertas = json.load(f)
    except:
        alertas = []

    alertas.append(mensaje)

    with open("app/alerts.json", "w") as f:
        json.dump(alertas[-10:], f)  # solo últimas 10 alertas

        estado_anterior = puertos



        time.sleep(30)