#include <EEPROM.h>

#define relay 8
#define lm35_0 A0
#define lm35_1 A1
#define lm35_2 A2
#define lm35_3 A3
#define lm35_4 A4
#define lm35_5 A5

String temp;
double temp0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);
  pinMode(lm35_0, INPUT);
  pinMode(lm35_1, INPUT);
  pinMode(lm35_2, INPUT);
  pinMode(lm35_3, INPUT);
  pinMode(lm35_4, INPUT);
  pinMode(lm35_5, INPUT);
}

void loop() {
  if (Serial.available()) {
    temp = Serial.readStringUntil('\n');

    if (temp.startsWith("clc")) {
      temp = "Received: " + temp + ", erasing EEPROM";
      Serial.println(temp);
      for (int i = 0 ; i < EEPROM.length() ; i++) {
        EEPROM.write(i, 0);
      }
    }

    else if (temp.startsWith("hlp")) {
      temp = "Received: " + temp + ", clc (clear EEPROM), get (get temperature data), cal (calibration)";
      Serial.println(temp);
    }

    else if (temp.startsWith("get")) {
      temp = "Received: " + temp;
      for (int i = 0; i < 12; i++) {
        temp = temp + ", " + EEPROM.read(i);
      }
      Serial.println(temp);
    }

    else if (temp.startsWith("cal"))  {
      temp = "Received: " + temp + ", starting the calibration";
      Serial.println(temp);

      digitalWrite(LED_BUILTIN, HIGH);
      digitalWrite(relay, HIGH);
      for (int i = 0; i < 20; i++) {
        delay(1250);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1250);
        digitalWrite(LED_BUILTIN, HIGH);
      }
      digitalWrite(LED_BUILTIN, LOW);
      digitalWrite(relay, LOW);
      temp0 = analogRead(lm35_0);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (0.9944 * temp0) - 1.7406;
      EEPROM.write(0, temp0);
      EEPROM.write(1, (temp0 - EEPROM.read(0)) * 100);
      temp0 = analogRead(lm35_1);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (1.0032 * temp0) - 2.3287;
      EEPROM.write(2, temp0);
      EEPROM.write(3, (temp0 - EEPROM.read(2)) * 100);
      temp0 = analogRead(lm35_2);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (0.9996 * temp0) + 2.2114;
      EEPROM.write(4, temp0);
      EEPROM.write(5, (temp0 - EEPROM.read(4)) * 100);
      temp0 = analogRead(lm35_3);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (0.9872 * temp0) + 1.3091;
      EEPROM.write(6, temp0);
      EEPROM.write(7, (temp0 - EEPROM.read(6)) * 100);
      temp0 = analogRead(lm35_4);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (0.9979 * temp0) + 2.4373;
      EEPROM.write(8, temp0);
      EEPROM.write(9, (temp0 - EEPROM.read(8)) * 100);
      temp0 = analogRead(lm35_5);
      temp0 = (5.0 * temp0 * 100.0) / 1023.0;
      temp0 = (0.9974 * temp0) + 0.6999;
      EEPROM.write(10, temp0);
      EEPROM.write(11, (temp0 - EEPROM.read(10)) * 100);
    }

    else {
      temp = "Received: " + temp + ", command not found; hlp for list";
      Serial.println(temp);
    }
  }
}
