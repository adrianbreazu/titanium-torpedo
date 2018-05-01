#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define GPIO_PIN 2
#define DEBUG false
#define VERBOSE false

extern "C" {
  #include "user_interface.h"
}

// WiFi connection details
const char* SSID = "__SSID__";
const char* PASSWORD = "__password__";
const char* PIN = "__pin__";
const char* KEY = "__key__";
const char* URL = "http://__ip_here__/sensors_actuators/ds18b20/";
const int TIME = 1800; //seconds
const uint32 SLEEP_TIME = TIME*1000000;

IPAddress IP(192,168,1,6);
IPAddress GATEWAY(192,168,1,1);
IPAddress SUBNET(255,255,255,0);
// no DNS needed
IPAddress DNS(0,0,0,0);

OneWire oneWire(GPIO_PIN);
DallasTemperature sensor(&oneWire);

void connect_wifi() {
  WiFi.mode(WIFI_STA);
  WiFi.config(IP,GATEWAY,SUBNET);
  WiFi.begin(SSID, PASSWORD);
  // make sure you are connected before going further
  while(WiFi.status() != WL_CONNECTED) {
    delay(100);
    if (DEBUG)
      Serial.print(".");
  }
  
  if (DEBUG) {
    Serial.println("");
    Serial.print("WiFi connected to ");
    Serial.println(SSID);
  }
}

void sendPOSTRequest() {
  char temperatureString[6];
  float temperatureFloat;
  String JSON_data = "";
  float temp_sum = 0;
  int number_of_reads = 7;
  if (VERBOSE)  
    Serial.println("#sendPOSTRequest, begin");

  if (WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    http.begin(URL);
    http.addHeader("Content-Type", "application/json");
    
    sensor.requestTemperatures();
    for (int i = 0; i< number_of_reads; i++) {
      temp_sum = temp_sum + sensor.getTempCByIndex(0);
      delay(500);
    }
    temperatureFloat = temp_sum / number_of_reads;
    dtostrf(temperatureFloat, 2, 2, temperatureString);
    
    
    if (DEBUG)
      Serial.println(temperatureString);

    JSON_data = "{ ";
    JSON_data += "\"pin\": \"";
    JSON_data += PIN;
    JSON_data += "\", \"key\": \"";
    JSON_data += KEY;
    JSON_data += "\", \"value\": \"";
    JSON_data += temperatureString;
    JSON_data += "\" }";

    int httpCode = http.POST(JSON_data);
    String response = http.getString();

    if (DEBUG) {
      Serial.println("Request data");
      Serial.println(JSON_data);
      
      Serial.print("post httpCode: ");
      Serial.println(httpCode);
      
      Serial.println("Response data");
      Serial.println(response);
    }

    http.end();
    delay(500);
    if (DEBUG)
      Serial.println("close connection");
  }else{
    if (DEBUG)
      Serial.println("error in WiFi connection");
  }

  if (VERBOSE)  
    Serial.println("#sendPOSTRequest, end");
}

void setup() {
  Serial.begin(115200);

  sensor.begin();
  connect_wifi();
  sendPOSTRequest();

  if (VERBOSE) {
    Serial.println("Finished Setup()");
    Serial.println(system_get_sdk_version());
  }
  delay(300);
  ESP.deepSleep(SLEEP_TIME);
}

void loop() {
  delay(500);
}
