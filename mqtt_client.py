import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import time
import threading

# Dados dos sensores (em memória)
sensor_data = {
    'temperature': 25.0,
    'humidity': 60,
    'presence': 0,
    'fan_status': 'OFF',
    'humidifier_status': 'OFF',
    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

def get_sensor_data():
    return sensor_data

def generate_test_data():
    """Gera dados de teste aleatórios"""
    global sensor_data
    while True:
        sensor_data = {
            'temperature': round(random.uniform(20, 35), 1),
            'humidity': random.randint(30, 80),
            'presence': random.randint(0, 1),
            'fan_status': random.choice(['ON', 'OFF']),
            'humidifier_status': random.choice(['ON', 'OFF']),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        time.sleep(3)
        print("Dados atualizados:", sensor_data)

def start_mqtt_client():
    """Inicia o gerador de dados de teste"""
    print("Modo de teste ativado - Gerando dados aleatórios...")
    thread = threading.Thread(target=generate_test_data, daemon=True)
    thread.start()