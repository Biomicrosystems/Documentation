#include <Arduino.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>
#include <WiFiGeneric.h>
#include <WiFiMulti.h>
#include <WiFiSTA.h>
#include <WiFiScan.h>
#include <WiFiServer.h>
#include <WiFiType.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

#define ONE_SECOND 1000
#define RXD2 16
#define TXD2 17

char ssid[] = "Okar";
char password[] = "7F9+e657";
String apiUrl = "http://45.61.54.143:3000";

String rawHeader = "{\"raw\":\"";
String identifierHeader = "\",\"identifier\":\"";
String deviceIdHeader = "\",\"deviceId\":\"";
String logHeader = "{\"info\":\"";
String commandNameHeader = "{\"name\":\"";
String closeBracket = "\"}";

String measurementResponse = "";
String identifier = "";
String rawData = "";

byte data_rcv[4];
byte start[3] = { 0xA0, 0x01, 0xAB };
byte sendData[6] = { 0xC0, 0xA0, 0x04, 0x04, 0x00, 0xAB };
byte end[3] = { 0xA0, 0x02, 0xAB };

int responseCode = 0;
int _resolution = 4096;
float voltage;
float current;

bool isRunning = false;
bool successfulRun = false;

byte c;

String deviceId = "dev-003";

HTTPClient http;

String command = "";

void setup() {

  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    logger("Attempting to connect to WPA SSID");
  }

  logger("You're connected to the network");
}

void loop() {

  if (command != "MEASUREMENT_IN_PROGRESS") {

    command = getCommand();
    delay(1000);
  }

  if (command == "STARTED_MEASUREMENT") {

    Serial2.write(sendData, 6);
    Serial2.write(start, 3);

    isRunning = true;
    measurementInProgress();
  }

  while ((Serial2.available() > 0) && isRunning) {

    c = Serial2.read();

    switch (c) {
      case 0xA0:
        while ((Serial2.peek() == -1))
          ;
        data_rcv[0] = Serial2.read();
        while ((Serial2.peek() == -1))
          ;
        data_rcv[1] = Serial2.read();
        while ((Serial2.peek() == -1))
          ;
        data_rcv[2] = Serial2.read();
        while ((Serial2.peek() == -1))
          ;
        data_rcv[3] = Serial2.read();

        voltage = ((data_rcv[0] << 6) & 0x0FC0) | data_rcv[1];
        current = ((data_rcv[2] << 6) & 0x0FC0) | data_rcv[3];

        voltage = (float)((voltage - (_resolution / 2)) * (3.3 / _resolution));
        current = (float)((current - (_resolution / 2)) * (3.3 / _resolution)) + 1.25;

        rawData += String(voltage, 10) + "|" + String(current, 10) + "_";

        successfulRun = true;
        break;
      case 0xB0:

        if (rawData != "") {

          Serial2.write(end, 3);

          http.begin(apiUrl + "/pawl/v1/api/measurement/");
          http.addHeader("Content-Type", "application/json");
          measurementResponse = rawHeader + rawData + identifierHeader + identifier + deviceIdHeader + deviceId + closeBracket;
          responseCode = http.POST(measurementResponse);

          rawData = "";
          isRunning = false;
        }

        if (successfulRun) {
          stopMeasurement();
        }

        logger("Measurement has been sent to the server");

        if (command == "MEASUREMENT_IN_PROGRESS") {

          Serial2.write(sendData, 6);
          Serial2.write(start, 3);
        }

        ESP.restart();
        ESP.restart();
        ESP.restart();
        break;

      default:
        break;
    }
  }
}

String getCommand() {

  String command = "";

  if ((WiFi.status() == WL_CONNECTED)) {

    HTTPClient http;

    http.begin(apiUrl + "/pawl/v1/api/command/" + deviceId);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.GET();

    if (httpCode == 200) {

      command = http.getString();
      DynamicJsonDocument commandJsonDocument(3072);
      DeserializationError gateErrorDeserialize = deserializeJson(commandJsonDocument, command);
      String commandName = commandJsonDocument["name"];
      String commandIdentifier = commandJsonDocument["identifier"];
      identifier = commandIdentifier;
      command = commandName;
    }

    http.end();
  }

  return command;
}

void logger(String log) {

  int responseCode = 0;
  String logData = "";

  HTTPClient http;
  http.begin(apiUrl + "/pawl/v1/api/pawl-logger/");
  http.addHeader("Content-Type", "application/json");

  logData = logHeader + log + closeBracket;

  responseCode = http.POST(logData);
}

void stopMeasurement() {

  int responseCode = 0;
  String commandRequest = "";

  HTTPClient http;
  http.begin(apiUrl + "/pawl/v1/api/command/" + deviceId);
  http.addHeader("Content-Type", "application/json");

  commandRequest = commandNameHeader + "STOPPED_MEASUREMENT" + identifierHeader + identifier + closeBracket;

  responseCode = http.PUT(commandRequest);
}

void measurementInProgress() {

  int responseCode = 0;
  String commandRequest = "";

  HTTPClient http;
  http.begin(apiUrl + "/pawl/v1/api/command/" + deviceId);
  http.addHeader("Content-Type", "application/json");

  commandRequest = commandNameHeader + "MEASUREMENT_IN_PROGRESS" + identifierHeader + identifier + closeBracket;

  responseCode = http.PUT(commandRequest);
}

void startMeasurement() {

  int responseCode = 0;
  String commandRequest = "";

  HTTPClient http;
  http.begin(apiUrl + "/pawl/v1/api/command/" + deviceId);
  http.addHeader("Content-Type", "application/json");

  commandRequest = commandNameHeader + "STARTED_MEASUREMENT" + identifierHeader + identifier + closeBracket;

  responseCode = http.PUT(commandRequest);
}
