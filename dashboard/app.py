#./app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import paho.mqtt.client as mqtt
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Configurações MQTT
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_ULTRASONIC = "/rover/sensors/ultrasonic"
MQTT_TOPIC_MPU6050 = "/rover/sensors/mpu6050"

ultrasonic_data = {}
mpu6050_data = {}

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_ULTRASONIC)
    client.subscribe(MQTT_TOPIC_MPU6050)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        sensor_data = json.loads(data["data"])
        if msg.topic == MQTT_TOPIC_ULTRASONIC:
            ultrasonic_data.update(sensor_data)
            socketio.emit('update_ultrasonic', ultrasonic_data, namespace='/test')
        elif msg.topic == MQTT_TOPIC_MPU6050:
            mpu6050_data.update(sensor_data)
            socketio.emit('update_mpu6050', mpu6050_data, namespace='/test')
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
    socketio.emit('update_ultrasonic', ultrasonic_data, namespace='/test')
    socketio.emit('update_mpu6050', mpu6050_data, namespace='/test')

if __name__ == '__main__':
    mqtt_client.loop_start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
