import subprocess
import platform
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def scan_wifi():
    """
    Scanne les réseaux Wi-Fi environnants.
    Compatible Windows (netsh) et Linux (iwlist).
    """
    os_type = platform.system()
    networks = []

    try:
        if os_type == "Windows":
            result = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if "SSID" in line:
                    ssid = line.split(":")[1].strip() if ":" in line else "Inconnu"
                    if ssid:
                        networks.append(ssid)
        elif os_type == "Linux":
            result = subprocess.run(["iwlist", "wlan0", "scan"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if "ESSID" in line:
                    ssid = line.split(":")[1].strip().replace('"', '')
                    if ssid:
                        networks.append(ssid)
        else:
            networks.append("⚠️ Système non supporté.")
    except Exception as e:
        networks.append(f"❌ Erreur : {e}")

    return networks

@app.route('/scan-wifi')
def scan_wifi_route():
    """Route Flask pour retourner les réseaux détectés."""
    nets = scan_wifi()
    return jsonify(nets)

if __name__ == "__main__":
    print("🚀 Serveur Flask en cours d'exécution... Accédez à http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
