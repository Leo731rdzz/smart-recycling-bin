// SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>
#include <Servo.h>
#include <DFRobotDFPlayerMini.h>

const int servoPin  = 9;
const int buzzerPin = 8;
const int buttonPin = 2;

DFRobotDFPlayerMini myDFPlayer;
Servo myServo;

// Variables para el control del botón y antirrebote (debounce)
int buttonState;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50; 

// Estado actual del servo (0 = 15°, 1 = 90°, 2 = 155°)
int servoPosState = 1; 

void set_servo(int angle) {
  angle = constrain(angle, 0, 180);
  myServo.write(angle);
  delay(600);
}

void buzz(int ms) {
  digitalWrite(buzzerPin, HIGH);
  delay(ms);
  digitalWrite(buzzerPin, LOW);
}

void play_audio(int trackNumber) {
  myDFPlayer.playMp3Folder(trackNumber);
}

void setup() {
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  pinMode(buttonPin, INPUT_PULLUP);

  myServo.attach(servoPin);
  myServo.write(90); 

  Serial1.begin(9600);
  
  // Desactivamos el ACK y el Reset automático
  myDFPlayer.begin(Serial1, false, false);
  myDFPlayer.volume(30);

  Bridge.begin();
  delay(2000);

  Bridge.provide("set_servo", set_servo);
  Bridge.provide("buzz", buzz);
  Bridge.provide("play_audio", play_audio);

  buzz(150);
  delay(200);
  buzz(150);
}

void loop() {
  // 1. Mantener comunicación con Python activa
  Bridge.update();

  // 2. Leer el estado del botón
  int reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == LOW) {
        servoPosState++; 
        if (servoPosState > 2) {
          servoPosState = 0; 
        }

        if (servoPosState == 0) {
          myServo.write(15);
        } else if (servoPosState == 1) {
          myServo.write(90);
        } else if (servoPosState == 2) {
          myServo.write(155);
        }
      }
    }
  }
  lastButtonState = reading;
}
