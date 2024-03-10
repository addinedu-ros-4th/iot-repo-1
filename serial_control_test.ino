#include <ArduinoJson.h>
#include <Wire.h>
#include <DHT.h>
#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_HUMI1 A0
#define SOIL_HUMI2 A2
#define TANK_WATER A3
#define HUMI_WATER A4

DHT dht(DHTPIN, DHTTYPE);

int cds_pin = A1;
int echo = 8;
int trig = 12;
int soil1, psoil1;
int soil2, psoil2;
int val, ledval, pledval;
int ledpin=3;

void setup() { 
 Serial.begin(9600);
 pinMode(trig, OUTPUT);
 pinMode(echo, INPUT);
 dht.begin();
 pinMode(ledpin, OUTPUT);
}

void loop() {  
 float h = dht.readHumidity();
 float t = dht.readTemperature();
 soil1 = analogRead(SOIL_HUMI1);
 psoil1 = map(soil1, 1023, 0, 0, 100);
 soil2 = analogRead(SOIL_HUMI2);
 psoil2 = map(soil2, 1023, 0, 0, 100);
 val = analogRead(cds_pin);
 ledval = map(val, 0, 1023, 255, 0);
 pledval = ledval * 0.4;
 
 digitalWrite(trig, HIGH);
 delayMicroseconds(10);
 digitalWrite(trig, LOW);
 float cycletime = pulseIn(echo, HIGH);
 float distance = ((340 * cycletime) / 10000) / 2;
 
 int tank = analogRead(TANK_WATER);
 int humi = analogRead(HUMI_WATER);

 StaticJsonDocument<200> doc;
 doc["temperature"] = t;
 doc["humidity"] = h;
 doc["soil_1"] = psoil1;
 doc["soil_2"] = psoil2;
 doc["led"] = pledval;
 doc["distance"] = distance;
 doc["tank"] = tank;
 doc["humi"] = humi;

 serializeJson(doc, Serial);
 Serial.println();

 // 데이터 전송 후, 짧은 대기 시간을 두고 수신 데이터 확인
 delay(100); // 데이터 수신 준비

 if (Serial.available()) {
   StaticJsonDocument<200> recvDoc;
   DeserializationError error = deserializeJson(recvDoc, Serial);
   
   if (!error) {
     String ledCommand = recvDoc["led"];
     
     if (ledCommand == "on") {
       digitalWrite(ledpin, HIGH); // LED 켜기
     } else if (ledCommand == "off") {
       digitalWrite(ledpin, LOW); // LED 끄기
     }
   }
 }

 delay(100); // 다음 데이터 측정 및 전송을 위한 대기
}
