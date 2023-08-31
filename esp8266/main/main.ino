#include <Arduino.h>
#include "WiFiManager.h"
#include "MqttManager.h"
#include "Config.h"

WiFiManager wifiManager(WIFI_SSID, WIFI_PASSWORD);
MqttManager mqttManager(MQTT_SERVER, MQTT_TOPIC, MQTT_CLIENT);

void setup() {
    Serial.begin(115200);

    wifiManager.connectWiFi();
    mqttManager.connectMQTT();
}

void loop() {
    mqttManager.publishDataFromSerial();
}
