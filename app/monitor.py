import time
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

        if nuevos and estado_anterior:

            mensaje = f"🚨 Nuevos puertos detectados: {list(nuevos)}"
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

        estado_anterior = puertos

        time.sleep(30)