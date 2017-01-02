// read more https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266WiFi
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi connection details
const char* ssid = "add_your_SSID_here";
const char* password = "add_your_PASSWORD_here";
const char* pin = "1234567890";
const char* key = "ABCDEFGH1234567890";
const char* URL = "http://192.168.100.114:8000/sensors_actuators/ds18b20/";


#define GPIO_PIN 2

OneWire oneWire(GPIO_PIN); // read more here http://playground.arduino.cc/Learning/OneWire

DallasTemperature sensor(&oneWire);
WiFiServer server(80);

void setup() {
    Serial.begin(115200);
    delay(100);

    sensor.begin();
    WiFi.begin(ssid, password);
    //debug
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    // make sure you are connected before going further
    while(WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    delay(500);
    server.begin();
    Serial.println("Web server running. Waiting for the ESP IP...");
    Serial.println(WiFi.localIP());
}

void loop() {
    char temperatureString[6];
    float temperatureFloat;
    String JSON_data = "";

    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      http.begin(URL);
      http.addHeader("Content-Type", "application/json");

      sensor.requestTemperatures();
      temperatureFloat = sensor.getTempCByIndex(0);
      dtostrf(temperatureFloat, 2, 2, temperatureString);
      Serial.println(temperatureString);

      JSON_data = "{ ";
      JSON_data += "\"pin\": \"";
      JSON_data += pin;
      JSON_data += "\", \"key\": \"";
      JSON_data += key;
      JSON_data += "\", \"value\": \"";
      JSON_data += temperatureString;
      JSON_data += "\" }";

      int httpCode = http.POST(JSON_data);
      String response = http.getString();

      Serial.println("Request data");
      Serial.println(JSON_data);
      Serial.println("Response data");
      Serial.println(response);

      http.end();
      delay(500);
      Serial.println("close connection");
    }else{
      Serial.println("error in WiFi connection");
    }

    //delay(10000); //debug purpose only
    delay(3600000);
}