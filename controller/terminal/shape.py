import paho.mqtt.publish as mqtt_publish
import uuid
import time
import json
import signal

# MQTT Configuration
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_TOPIC_CONTROLLER = "/rover/controller"

# Velocidade média em km/h
VELOCIDADE_MEDIA_KMH = 2.65

# Generate a random user ID
user_id = str(uuid.uuid4())

def generate_message_id():
    return str(uuid.uuid4())

# Define a global para armazenar o tempo inicial
tempo_inicial = None

# Define a MQTT message payload for movement commands
def create_payload(direction):
    message_id = generate_message_id()
    timestamp_micros = int(time.time() * 1e6)  # Microseconds since epoch
    payload = {
        "user_id": user_id,
        "message_id": message_id,
        "direction": direction,
        "speed": 50,
        "timestamp_micros": timestamp_micros  # Include micros
    }
    return payload

# Define a function to send a sequence of movement commands based on the selected shape
def send_shape_commands(shape):
    global tempo_inicial
    commands = []
    if shape == "circle":
        commands = ["FORWARD", "RIGHT", "FORWARD", "RIGHT", "FORWARD", "RIGHT", "FORWARD", "RIGHT", "STOP"]
    elif shape == "square":
        commands = ["FORWARD", "RIGHT", "FORWARD", "RIGHT", "FORWARD", "RIGHT", "FORWARD", "RIGHT", "STOP"]
    elif shape == "triangle":
        commands = ["FORWARD", "LEFT", "FORWARD", "LEFT", "FORWARD", "LEFT", "STOP"]
    elif shape == "1":
        commands = ["FORWARD", "FORWARD", "LEFT", "STOP"]

    distancia_percorrida_km = 0.0
    distancia_percorrida_cm = 0.0
    
    for command in commands:
        if tempo_inicial is None:
            tempo_inicial = time.time()
        
        payload = create_payload(command)
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=json.dumps(payload), hostname=MQTT_BROKER_HOST)
        print(f"Enviado comando: {command}")
        
        # Calcula o tempo decorrido desde o início
        tempo_decorrido = time.time() - tempo_inicial
        
        # Calcula a distância percorrida em km
        distancia_percorrida_km = VELOCIDADE_MEDIA_KMH * (tempo_decorrido / 3600)
        
        # Calcula a distância em cm (1 km = 100.000 cm)
        distancia_percorrida_cm = distancia_percorrida_km * 100000
        
        time.sleep(0.3)  # Aguarda 0.3 segundos entre os comandos
    
    print(f"Distância percorrida em km: {distancia_percorrida_km:.4f} km")
    print(f"Distância percorrida em cm: {distancia_percorrida_cm:.2f} cm")

def signal_handler(signal, frame):
    print("Programa interrompido.")
    exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)  # Configura o manipulador de sinal

    print("Digite o nome da figura geométrica (circle, square, triangle ou 1) e pressione Enter:")
    shape_name = input().lower()

    if shape_name in ["circle", "square", "triangle", "1"]:
        send_shape_commands(shape_name)
    else:
        print("Figura geométrica desconhecida. Use 'circle', 'square', 'triangle' ou '1'.")

if __name__ == "__main__":
    main()
