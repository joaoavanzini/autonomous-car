#include "MqttManager.h"
#include "Config.h"

MqttManager::MqttManager(const char* mqttServer, const char* mqttTopic, const char* mqttClient)
        : mqttServer(mqttServer), mqttTopic(mqttTopic), mqttClient(mqttClient), client(espClient) {
}

void MqttManager::connectMQTT() {
    client.setServer(mqttServer, 1883);
}

void MqttManager::publishDataFromSerial() {
    if (client.connect(mqttClient)) {
        Serial.println("Connected to MQTT server!");
        while (client.state() == MQTT_CONNECTED) {
            memset(dataJson, 0, 256);
            String myStr = Serial.readStringUntil('\n');
            myStr.toCharArray(dataJson, myStr.length() + 1);
            if (myStr != "") {
                client.publish(mqttTopic, dataJson);
                Serial.println("Published data-JSON!");
            }
        }
    } else {
        Serial.println("Disconnected from MQTT server!");
        delay(MAX_DELAY);
    }
}
