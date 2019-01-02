#include <ESP8266WiFi.h>
#include <Wire.h>
#include <OneWire.h>
#include <Adafruit_BMP085.h>
#include <DallasTemperature.h>
#include <LiquidCrystal_PCF8574.h>
#include <PubSubClient.h>
#include <ESP8266HTTPClient.h>
#include "WiFi.h"
#include "Sensor.h"

#define TEMP_SENSOR 2
#define DEBUG true //false
#define VERBOSE true //false
#define LCD false

const int SLEEP_TIME_S = 1800;
const int NO_WIFI_SLEEP_TIME_S = 600;
const int BMP_CONNECT_COUNT = 10;
const int WIFI_CONNECT_COUNT = 30;
const int DS18B20_READ_ATTEMPTS_COUNT = 10;


OneWire oneWire(TEMP_SENSOR);
DallasTemperature temp_sensor(&oneWire);
Adafruit_BMP085 bmp_sensor;
LiquidCrystal_PCF8574 lcd(0x27);

char temperatureCString[6];
float vcc = 0.0f;
float lsb = 0.006206897f; //value set for 4 x AA batteries
int adc = 0;
char vcc_value[6];

void getTemperature();
void sendJsonDS18B20 ();
void sendJsonBMP180();
void sendJsonVcc();
bool useBMP = true;
bool useDS18B20 = true;

void setup() {
// -------------------- init Serial --------------------
  if (DEBUG)
    Serial.begin(115200);

// -------------------- init LCD --------------------
  if (LCD) {
    Wire.begin();  
    if (DEBUG)
      Serial.println("Init LCD");
    Wire.beginTransmission(0x27);
    int error = Wire.endTransmission();
    if (DEBUG) {
      if (error = 0)
        Serial.println("Not LCD found !");
      else
        Serial.println("Finished LCD init.");
    }
    lcd.begin(16,2);
    lcd.setBacklight(255);
    lcd.home();
    lcd.clear();
    lcd.print("READY");
  }

// -------------------- init BMP180 --------------------
  useBMP = bmp_sensor.begin();
  if(!useBMP) {
    if (DEBUG)
      Serial.println("Could not find a avalid BMP180 sensor");
    int bmp_count = 0;
    while (bmp_count < BMP_CONNECT_COUNT && !useBMP) {
      delay(500);
      bmp_count++;
      useBMP = bmp_sensor.begin();
      Serial.print("BMP status: ");
      Serial.println(useBMP);
    }
  }
  if (VERBOSE)
    Serial.println("BMP180 setup finished");
  if (LCD) {
    lcd.clear();
    lcd.print("BMP180 READY");
  }

// -------------------- init DS18B20 --------------------
  temp_sensor.begin();
  if (VERBOSE)
    Serial.println("DS18B20 setup finished");
  if (LCD) {
    lcd.clear();
    lcd.print("DS18B20 READY");
  }

// -------------------- init WiFi --------------------
  if (VERBOSE)
    Serial.println("Start setup WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.config(IP,GATEWAY,SUBNET);
  WiFi.begin(SSID, PASSWORD);
  int wifi_count = 0;
  while (WiFi.status() != WL_CONNECTED && wifi_count < WIFI_CONNECT_COUNT) {
    delay(500);
    wifi_count++;
    if (DEBUG)
      Serial.print(".");
  }

// -------------------- send data if connected to WiFi --------------------
  if (wifi_count < WIFI_CONNECT_COUNT) {
    if (DEBUG)
      Serial.println("");
      Serial.println("WiFi connected");
    if (VERBOSE) {
      Serial.println("WiFi setup finished");
      Serial.println(WiFi.localIP());
    }
    if (LCD) {
      lcd.clear();
      lcd.print("WiFi READY");
    }
    
    if (DEBUG)
      Serial.println("begin sending data");
  
    getTemperature();
    if (useDS18B20)
      sendJsonDS18B20();
    if (useBMP)
      sendJsonBMP180();
    sendJsonVcc();
    if (LCD)
      DisplayData();
  
    // cleanup and go to sleep
    if (DEBUG)
      Serial.println("Put ESP8266 in sleep mode");
    if (LCD) {
      lcd.clear();
      lcd.print("Go to sleep");
    }
    
    if (VERBOSE)
      Serial.println("#setup, before sleep");
    delay(500);
    ESP.deepSleep(SLEEP_TIME_S * 1000000);
  }
// -------------------- go back to sleep if unable to connect to WiFi --------------------
  else {
    if (DEBUG) {
      Serial.print("No WiFi go back in sleep for ");
      Serial.print(NO_WIFI_SLEEP_TIME_S);
      Serial.println(" seconds !");
    }
    if (VERBOSE)
      Serial.println("#setup, before sleep no WiFi");
    delay(500);
    ESP.deepSleep(NO_WIFI_SLEEP_TIME_S * 1000000);
  }

  if (VERBOSE)
    Serial.println("#setup, end");
}

void loop() {
  delay(300);
}

void getTemperature() {
  if (VERBOSE)
    Serial.println("#getTemperature, begin");
  float tempC;
  int read_attempt_count = 0;
  do {
    temp_sensor.requestTemperatures();
    tempC = temp_sensor.getTempCByIndex(0);
    dtostrf(tempC, 2, 2, temperatureCString);
    delay(100);
    read_attempt_count++;
  } while ((tempC == 85.0 || tempC == (-127.0)) && read_attempt_count < DS18B20_READ_ATTEMPTS_COUNT);
  if (tempC == 85.0 || tempC == (-127.0))
    useDS18B20 = false;
  else
    useDS18B20 = true;
  if (VERBOSE)
    Serial.println("#getTemperature, end");
}

void sendJsonDS18B20() {
  if (VERBOSE)
    Serial.println("#sendJsonTemp, begin");
  String JSON_data = "";

  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    http.begin(URL_DS18B20);
    http.addHeader("Content-Type", "application/json");

    JSON_data = "{ ";
    JSON_data += "\"pin\": \"";
    JSON_data += PIN_DS18B20;
    JSON_data += "\", \"key\": \"";
    JSON_data += KEY_DS18B20;
    JSON_data += "\", \"value\": \"";
    JSON_data += temperatureCString;
    JSON_data += "\" }";

    int httpCode = http.POST(JSON_data);
    if (DEBUG) {
      Serial.println();
      Serial.println("httpCode:");
      Serial.println(httpCode);
    }
    String response = http.getString();
    if (DEBUG) {
      Serial.println("Request data");
      Serial.println(JSON_data);
      Serial.println("Response data");
      Serial.println(response);
    }
    
    http.end();
    delay(500);
    if (DEBUG)
      Serial.println("close connection");
  } else {
    if (DEBUG)
      Serial.println("error in WiFi connection");
  }
  if (VERBOSE)
    Serial.println("#sendJsonTemp, end");
}

void sendJsonData(String pin, String key, String value, String type) {
  if (VERBOSE)
    Serial.println("#sendJsonData, begin");
    
  String JSON_data = "";
  
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    http.begin(URL_SENSOR);
    http.addHeader("Content-Type", "application/json");

    JSON_data = "{ ";
    JSON_data += "\"pin\": \"";
    JSON_data += pin;
    JSON_data += "\", \"key\": \"";
    JSON_data += key;
    JSON_data += "\", \"value\": \"";
    JSON_data += value;
    JSON_data += "\", \"type\": \"";
    JSON_data += type;
    JSON_data += "\" }";

    int httpCode = http.POST(JSON_data);
    if (DEBUG) {
      Serial.println();
      Serial.println("httpCode:");
      Serial.println(httpCode);
    }
    String response = http.getString();
    if (DEBUG) {
      Serial.println("Request data");
      Serial.println(JSON_data);
      Serial.println("Response data");
      Serial.println(response);
    }
    
    http.end();
    delay(500);
    if (DEBUG)
      Serial.println("close connection");
  } else {
    if (DEBUG)
      Serial.println("error in WiFi connection");
  }
  if (VERBOSE)
    Serial.println("#sendJsonData, end");
}

void sendJsonBMP180() {
  if (VERBOSE)
    Serial.println("#sendJsonBMP180, begin");
  
  char value[10];
  
  dtostrf(bmp_sensor.readTemperature(), 2, 2, value);
  sendJsonData(PIN_BMP180_TEMP, KEY_BMP180_TEMP, value, "temperature");

  dtostrf(bmp_sensor.readPressure(), 2, 2, value);
  sendJsonData(PIN_BMP180_PRES, KEY_BMP180_PRES, value, "pressure");

  dtostrf(bmp_sensor.readAltitude(), 2, 2, value);
  sendJsonData(PIN_BMP180_ALT, KEY_BMP180_ALT, value, "altitude");
  
  if (VERBOSE)
    Serial.println("#sendJsonBMP180, end");
}

void sendJsonVcc() {
  if (VERBOSE)
    Serial.println("#sendJsonVcc, begin");
    
  String JSON_message = "";
  
  adc = analogRead(A0);
  if (DEBUG) {
    Serial.print("adc= ");
    Serial.println(adc);
  }
  
  vcc = adc*lsb;
  if (DEBUG) {
    Serial.print("Vcc = ");
    Serial.println(vcc);
  }
  
  dtostrf(vcc, 2, 2, vcc_value);
  sendJsonData(PIN_VCC, KEY_VCC, vcc_value, "vcc");
  
  if (VERBOSE)
    Serial.println("#sendJsonVcc, end");
}

void DisplayData() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T=");
  lcd.setCursor(3, 0);
  lcd.print(bmp_sensor.readTemperature());
  lcd.setCursor(8, 0);
  lcd.print( "|");
  lcd.setCursor(9, 0);
  lcd.print("P=");
  lcd.setCursor(11, 0);
  lcd.print(bmp_sensor.readPressure());

  lcd.setCursor(0, 1);
  lcd.print("T=");
  lcd.setCursor(3, 1);
  lcd.print(temperatureCString);
  lcd.setCursor(8, 1);
  lcd.print( "|");
  lcd.setCursor(9, 1);
  lcd.print("S=");
  lcd.setCursor(11, 1);
  lcd.print(bmp_sensor.readAltitude(102000));
}

