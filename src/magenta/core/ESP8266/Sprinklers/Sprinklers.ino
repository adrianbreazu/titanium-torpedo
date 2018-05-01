#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include "GPIO.h"
#include "Sensor.h"

#define DEBUG true //false
#define VERBOSE false

ESP8266WebServer server(80);

void setupRelays();
void connectToWiFi();
void setupRoutes();
void getState();
void setState();
void resetState();

void setup() {
// -------------------- init Serial --------------------
  if (DEBUG) {
    Serial.begin(115200);
    Serial.println();
    Serial.println("--- --- ---");
    Serial.println("Finish serial setup");
    delay(10);
  }

  setupRelays();
  delay(10);
  connectToWiFi();

  setupRoutes();

  if (VERBOSE)
    Serial.println("Finish setup");
}

void loop() {
  if (VERBOSE)
    Serial.println("Begin loop");

    server.handleClient();

  if (VERBOSE)
    Serial.println("Finish loop");
}

void setupRelays(void) {
  if (VERBOSE)
    Serial.println("Begin setupRelays");

  if (DEBUG)
    Serial.println("Begin GPIO set mode");
  pinMode(GPIO_A, OUTPUT);
  pinMode(GPIO_B, OUTPUT);
  pinMode(GPIO_C, OUTPUT);
  pinMode(GPIO_D, OUTPUT);
  pinMode(GPIO_E, OUTPUT);
  if (DEBUG)
    Serial.println("Finish GPIO set mode");

  if (VERBOSE)
    Serial.println("Finish setupRelays");
}

void connectToWiFi() {
  if (VERBOSE)
    Serial.println("Begin connectToWiFi");

  WiFi.mode(WIFI_STA);
  WiFi.config(IP,GATEWAY,SUBNET);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    if (DEBUG)
      Serial.print(".");
  }

  if (DEBUG)
      Serial.println();
      Serial.println("WiFi connected");
  if (VERBOSE) {
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  }

  if (VERBOSE)
    Serial.println("End connectToWiFi");
}

void setupRoutes() {
  server.on("/getState", getState);
  server.on("/setState", setState);
  server.on("/reset", resetState);
  server.on("/heartBeat", [](){server.send(200,"text/plain", "Still alive!");});
  server.begin();
}

void getState() {
  if (VERBOSE)
    Serial.println("Begin getState");

  String data = server.arg("plain");
  if (DEBUG)
    Serial.println(data);

  StaticJsonBuffer<200> jBuffer;
  JsonObject& jObject = jBuffer.parseObject(data);
  String secret_key = jObject["SECRET_KEY"];
  if (secret_key == SECRET_KEY) {
    Serial.println("authenticated request. prepare to send state");
    StaticJsonBuffer<200> jBuffer_response;
    JsonObject& jRoot = jBuffer_response.createObject();
    jRoot["Relay_A"] = digitalRead(GPIO_A);
    jRoot["Relay_B"] = digitalRead(GPIO_B);
    jRoot["Relay_C"] = digitalRead(GPIO_C);
    jRoot["Relay_D"] = digitalRead(GPIO_D);
    jRoot["Relay_E"] = digitalRead(GPIO_E);

    String output;
    jRoot.printTo(output);
    server.send(202, "text/json", output);
  }
  else {
    if (DEBUG)
      Serial.println("unauthenticated request !");
      server.send(404, "Fail");
  }

  if (VERBOSE)
    Serial.println("Finish getState");
}

void setState() {
  if (VERBOSE)
    Serial.println("Begin setState");

  String data = server.arg("plain");
  if (DEBUG)
    Serial.println(data);

  StaticJsonBuffer<200> jBuffer;
  JsonObject& jObject = jBuffer.parseObject(data);
  String secret_key = jObject["SECRET_KEY"];
  const char* relay = jObject.get<const char*>("Relay");
  bool state = jObject.get<bool>("State");
  if (secret_key == SECRET_KEY) {
    Serial.println();
    Serial.print("authenticated request. prepare to set state for relay: ");
    Serial.print(relay);
    switch (relay[0]) {
      case 'A':
        if (DEBUG) {
          Serial.println();
          Serial.print("Set GPIO_A state: ");
          Serial.println(state);
        }
        state ? digitalWrite(GPIO_A,HIGH) : digitalWrite(GPIO_A, LOW);
        break;
      case 'B':
        if (DEBUG) {
          Serial.println();
          Serial.print("Set GPIO_B state: ");
          Serial.println(state);
        }
        state ? digitalWrite(GPIO_B,HIGH) : digitalWrite(GPIO_B, LOW);
        break;
      case 'C':
        if (DEBUG) {
          Serial.println();
          Serial.print("Set GPIO_C state: ");
          Serial.println(state);
        }
        state ? digitalWrite(GPIO_C,HIGH) : digitalWrite(GPIO_C, LOW);
        break;
      case 'D':
        if (DEBUG) {
          Serial.println();
          Serial.print("Set GPIO_D state: ");
          Serial.println(state);
        }
        state ? digitalWrite(GPIO_D,HIGH) : digitalWrite(GPIO_D, LOW);
        break;
      case 'E':
        if (DEBUG) {
          Serial.println();
          Serial.print("Set GPIO_E state: ");
          Serial.println(state);
        }
        state ? digitalWrite(GPIO_E, HIGH) : digitalWrite(GPIO_E, LOW);
        break;
      default:
        digitalWrite(GPIO_A, LOW);
        digitalWrite(GPIO_B, LOW);
        digitalWrite(GPIO_C, LOW);
        digitalWrite(GPIO_D, LOW);
        digitalWrite(GPIO_E, LOW);
    }
    StaticJsonBuffer<200> jBuffer_response;
    JsonObject& jRoot = jBuffer_response.createObject();
    jRoot["Relay_A"] = digitalRead(GPIO_A);
    jRoot["Relay_B"] = digitalRead(GPIO_B);
    jRoot["Relay_C"] = digitalRead(GPIO_C);
    jRoot["Relay_D"] = digitalRead(GPIO_D);
    jRoot["Relay_E"] = digitalRead(GPIO_E);

    String output;
    jRoot.printTo(output);
    server.send(202, "text/json", output);
  }
  else {
    if (DEBUG)
      Serial.println("unauthenticated request !");
      server.send(404, "Fail");
  }

  if (VERBOSE)
    Serial.println("Finish setState");
}

void resetState() {
  if (VERBOSE)
    Serial.println("Begin resetState");

  String data = server.arg("plain");
  if (DEBUG)
    Serial.println(data);

  digitalWrite(GPIO_A, LOW);
  digitalWrite(GPIO_B, LOW);
  digitalWrite(GPIO_C, LOW);
  digitalWrite(GPIO_D, LOW);
  digitalWrite(GPIO_E, LOW);

  StaticJsonBuffer<200> jBuffer_response;
  JsonObject& jRoot = jBuffer_response.createObject();
  jRoot["Relay_A"] = digitalRead(GPIO_A);
  jRoot["Relay_B"] = digitalRead(GPIO_B);
  jRoot["Relay_C"] = digitalRead(GPIO_C);
  jRoot["Relay_D"] = digitalRead(GPIO_D);
  jRoot["Relay_E"] = digitalRead(GPIO_E);

  String output;
  jRoot.printTo(output);
  server.send(202, "text/json", output);

  if (VERBOSE)
    Serial.println("Finish resetState");
}
