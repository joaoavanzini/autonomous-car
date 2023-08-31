#include "WiFiManager.h"
#include "Config.h"

WiFiManager::WiFiManager(const char* ssid, const char* password)
        : ssid(ssid), password(password) {
}

void WiFiManager::connectWiFi() {
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to WiFi, IP address: ");
    Serial.println(WiFi.localIP());
}
