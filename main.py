from machine import Pin
import dht
import time
import network
from umqtt.simple import MQTTClient
import config

# Configuração dos sensores e atuadores
sensor_dht = dht.DHT11(Pin(config.PIN_DHT))
sensor_pir = Pin(config.PIN_PIR, Pin.IN)
relay = Pin(config.PIN_RELAY, Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando à rede Wi-Fi...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
            print('.', end='')
    print('\nConectado! IP:', wlan.ifconfig()[0])

def connect_mqtt():
    client = MQTTClient("esp32_client", config.MQTT_BROKER, 
                       user=config.MQTT_USER, password=config.MQTT_PASSWORD)
    client.connect()
    print("Conectado ao broker MQTT")
    return client

def read_sensors():
    try:
        sensor_dht.measure()
        temperature = sensor_dht.temperature()
        humidity = sensor_dht.humidity()
        presence = sensor_pir.value()
        return temperature, humidity, presence
    except Exception as e:
        print("Erro na leitura dos sensores:", e)
        return None, None, None

def main():
    connect_wifi()
    mqtt_client = connect_mqtt()
    
    print("Sistema IoT iniciado. Enviando dados...")
    
    while True:
        try:
            temp, humid, presence = read_sensors()
            
            if temp is not None:
                # Publica dados nos tópicos MQTT
                mqtt_client.publish(config.TOPIC_TEMP, str(temp))
                mqtt_client.publish(config.TOPIC_HUMID, str(humid))
                mqtt_client.publish(config.TOPIC_PRESENCE, str(presence))
                
                print(f"Temp: {temp}°C, Umidade: {humid}%, Presença: {presence}")
            
            time.sleep(5)  # Espera 5 segundos entre leituras
            
        except Exception as e:
            print("Erro no loop principal:", e)
            time.sleep(10)
            # Tentar reconectar
            try:
                mqtt_client = connect_mqtt()
            except:
                print("Falha ao reconectar")

if __name__ == "__main__":
    main()