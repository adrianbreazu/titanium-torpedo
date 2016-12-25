// read more https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266WiFi

#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi connection details
const char* SSID = "add_your_SSID_here";
const char* PASSWORD = "add_your_PASSWORD_here";

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

    String string_data = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
    string_data += "<!DOCTYPE HTML>\r\n<html>\r\n";
    string_data += "<head><title>DS18B20 Temperature Data</title></head>";
    string_data += "<body><h1>Temperature *C</h1><br/><p>The temperature at your location is :";
    string_data += temperatureString;
    string_data += " *C </p><br/><br/><p>Thank you for using this</p></body>";
    string_data += "<footer><p>2016 titanium-torpedo github project</p></footer>";
    string_data += "</html>\n";

    client.print(string_data);
    delay(500);
    client.stop();
}