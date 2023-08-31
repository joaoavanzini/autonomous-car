#ifndef MQTT_MANAGER_H
#define MQTT_MANAGER_H

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

class MqttManager {
public:
    MqttManager(const char* mqttServer, const char* mqttTopic, const char* mqttClient);
    void connectMQTT();
    void publishDataFromSerial();

private:
    const char* mqttServer;
    const char* mqttTopic;
    const char* mqttClient;
    WiFiClient espClient;
    PubSubClient client;
    char dataJson[256];
};

#endif
