import smtplib
from email.mime.text import MIMEText

def enviar_alerta(mensaje):

    remitente = "TU_CORREO@gmail.com"
    clave = "TU_PASSWORD_APP"
    destino = "DESTINO@gmail.com"

    msg = MIMEText(mensaje)
    msg["Subject"] = "🚨 Alerta SecureScan"
    msg["From"] = remitente
    msg["To"] = destino

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remitente, clave)
        server.send_message(msg)