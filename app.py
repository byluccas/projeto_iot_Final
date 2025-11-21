# app.py - Versão corrigida com estrutura de pastas
from flask import Flask, render_template, jsonify
import threading
import random
import socket
from datetime import datetime

app = Flask(__name__)

# Dados dos sensores
sensor_data = {
    "temperature": 25.0,
    "humidity": 60,
    "presence": 0,
    "fan_status": "OFF",
    "humidifier_status": "OFF",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


def generate_test_data():
    global sensor_data
    while True:
        sensor_data = {
            "temperature": round(random.uniform(20, 35), 1),
            "humidity": random.randint(30, 80),
            "presence": random.randint(0, 1),
            "fan_status": random.choice(["ON", "OFF"]),
            "humidifier_status": random.choice(["ON", "OFF"]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        print("Dados atualizados:", sensor_data)
        threading.Event().wait(3)


@app.route("/")
def index():
    return render_template("dashboard.html", data=sensor_data)


@app.route("/api/data")
def api_data():
    return jsonify(sensor_data)


@app.route("/api/control/<device>/<state>", methods=["POST"])
def control_device(device, state):
    if device == "ventilador":
        sensor_data["fan_status"] = state.upper()
    elif device == "umidificador":
        sensor_data["humidifier_status"] = state.upper()
    return jsonify({"status": "success"})


def find_available_port(start_port=5000, end_port=9000):
    for port in range(start_port, end_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", port))
                return port
        except:
            continue
    return 8000 


if __name__ == "__main__":
    thread = threading.Thread(target=generate_test_data, daemon=True)
    thread.start()
    
    port = find_available_port()
    print(f"🎯 Usando porta: {port}")
    print(f"🌐 Acesse: http://localhost:{port}")
    print("🛑 Para parar: Ctrl+C")

    try:
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        print(f"❌ Erro na porta {port}: {e}")
        port = 8000
        print(f"🔄 Tentando porta {port}...")
        app.run(host="0.0.0.0", port=port, debug=False)
