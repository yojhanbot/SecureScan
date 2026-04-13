import re

def analizar(resultado):

    riesgos = []
    recomendaciones = []

    puertos = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", resultado)
    puertos_abiertos = [p[0] for p in puertos]

    for puerto, servicio in puertos:

        if puerto == "22":
            riesgos.append("🔴 SSH expuesto (acceso remoto)")
            recomendaciones.append("💡 Usar autenticación por clave y deshabilitar root")

        elif puerto == "80":
            riesgos.append("🟡 HTTP activo (sin cifrado)")
            recomendaciones.append("💡 Redirigir tráfico a HTTPS")

        elif puerto == "443":
            riesgos.append("🟢 HTTPS activo")
            recomendaciones.append("💡 Verificar certificado SSL válido")

        elif puerto == "3306":
            riesgos.append("🚨 Base de datos expuesta")
            recomendaciones.append("💡 Restringir acceso a IPs internas")

        else:
            riesgos.append(f"🟠 Puerto {puerto} ({servicio}) abierto")
            recomendaciones.append("💡 Revisar si este servicio es necesario")

    # 🔥 Interferencias inteligentes
    if "80" in puertos_abiertos and "443" in puertos_abiertos:
        recomendaciones.append("⚠️ Configurar redirección automática de HTTP a HTTPS")

    if not riesgos:
        riesgos.append("🟢 No se detectaron riesgos importantes")
        recomendaciones.append("💡 Sistema correctamente configurado")

    return riesgos, recomendaciones