import subprocess

def escanear(ip):
    try:
        resultado = subprocess.run(
            ["nmap", "-sT", "-F", "--min-rate", "1000", ip],
            capture_output=True,
            text=True,
            timeout=15
        )
        return resultado.stdout

    except subprocess.TimeoutExpired:
        return "⚠️ El escaneo tardó demasiado (timeout)"

    except Exception as e:
        return f"Error: {e}"