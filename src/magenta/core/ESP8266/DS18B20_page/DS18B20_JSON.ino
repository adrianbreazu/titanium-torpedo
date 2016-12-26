// read more https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266WiFi

#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi connection details
const char* SSID = "add_your_SSID_here";
const char* PASSWORD = "add_your_PASSWORD_here";
const char* PIN = "12345abcde";
const char* ID = "add_IoT_ID_here";
const char* TYPE = "Sensor_Type";

#define GPIO_PIN 2

OneWire oneWire(GPIO_PIN); // read more here http://playground.arduino.cc/Learning/OneWire

DallasTemperature sensor(&oneWire);
WiFiServer server(80);

void setup() {

    sensor.begin();
    WiFi.begin(SSID, PASSWORD);

    // make sure you are connected before going further
    while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    }

    delay(500);

    server.begin();
}

void loop() {
    char temperatureString[6];
    float temperatureFloat;
    String JSON_data;

    WiFiClient client = server.available();

    if (!client) {
        return;
    }

    while (!client.available()) {
        delay(10);
    }

    client.flush();

    temperatureFloat = sensor.getTempCByIndex(0);
    dtostrf(temperatureFloat, 2, 2, temperatureString);

    JSON_data = '{ "id": "';
    JSON_data += ID;
    JSON_data += '", "pin": "';
    JSON_data += PIN;
    JSON_data += '", "type": "';
    JSON_data += TYPE;
    JSON_data += '", "data": "';
    JSON_data += temperatureString;
    JSON_data += '" }';

    String string_data = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n";
    string_data += "Connection: close\r\n";
    string_data += "Content-Length: ";
    string_data += JSON_data.length();
    string_data += "\r\n\r\n";
    string_data += JSON_data;
    string_data += "\n";

    client.print(string_data);
    delay(500);
    client.stop();
}