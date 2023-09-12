from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

# Configurações MQTT
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "/rover/ultrasonic"

ultrasonic_data = {
    "left": [],
    "center": [],
    "right": []
}

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        sensor_data = json.loads(data["data"])
        ultrasonic_data["left"].append(sensor_data["left"])
        ultrasonic_data["center"].append(sensor_data["center"])
        ultrasonic_data["right"].append(sensor_data["right"])
        socketio.emit('update', {'left': sensor_data["left"], 'center': sensor_data["center"], 'right': sensor_data["right"]}, namespace='/test')
    except Exception as e:
        print("Erro ao processar a mensagem MQTT:", str(e))

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # Envia os valores iniciais para a página quando um cliente se conecta
    socketio.emit('update', {'left': ultrasonic_data["left"][-1], 'center': ultrasonic_data["center"][-1], 'right': ultrasonic_data["right"][-1]}, namespace='/test')

if __name__ == '__main__':
    mqtt_client.loop_start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
