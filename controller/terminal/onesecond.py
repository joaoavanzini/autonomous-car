import paho.mqtt.publish as mqtt_publish
import time
import json
import uuid  # Importe o módulo uuid

# MQTT Configuration
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_TOPIC_CONTROLLER = "/rover/controller"

# Define a função para criar a carga MQTT para os comandos FORWARD e STOP
def create_payload(direction, speed):
    message_id = str(uuid.uuid4())
    timestamp_micros = int(time.time() * 1e6)  # Microssegundos desde o epoch
    payload = {
        "user_id": user_id,
        "message_id": message_id,
        "direction": direction,
        "speed": speed,
        "timestamp_micros": timestamp_micros  # Inclua os microssegundos
    }
    return payload

# Gere um ID de usuário aleatório
user_id = str(uuid.uuid4())

# Crie as cargas FORWARD e STOP
forward_payload = create_payload("FORWARD", 100)
stop_payload = create_payload("STOP", 0)

# Função para publicar mensagens MQTT
def publish(payload):
    mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=json.dumps(payload), hostname=MQTT_BROKER_HOST)
    print(f"Publicado: {payload}")

# Envie o comando FORWARD
publish(forward_payload)

# Aguarde 1 segundo
time.sleep(1)

# Envie o comando STOP após 1 segundo
publish(stop_payload)
