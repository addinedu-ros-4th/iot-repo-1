#include <ArduinoJson.h> //라이브러리 설치 필요
#include <Wire.h> 
#include <DHT.h> // 온습도센서 라이브러리 
#include <Servo.h> //Servo 라이브러리

#define DHTPIN 4 // 온습도센서 핀번호
#define SOIL_HUMI1 A0
#define SOIL_HUMI2 A1
#define TANK_WATER A2
#define DHTTYPE DHT11

int cds_pin = A3; // 조도센서에 사용할 핀번호
int soil_humi1, psoil_humi1;
int soil_humi2, psoil_humi2;
int ledpin = 3; // LED에 사용할 핀번호
int val, ledval, pledval; // 조도센서 값을 사용하기 위한 변수 선언
int echo1 = 5; // 초음파센서1
int trig1 = 6; // 초음파센서1
int echo2 = 7; // 초음파센서1
int trig2 = 8; // 초음파센서1

DHT dht(DHTPIN, DHTTYPE); // 온습도센서 사용 설정

void setup() { 
 Serial.begin(9600); 
 Serial.println("화분1 START!"); //시리얼 모니터에 문자 출력
 pinMode(trig1, OUTPUT);
 pinMode(echo1, INPUT); 
 pinMode(trig2, OUTPUT);
 pinMode(echo2, INPUT); 
 pinMode(ledpin, OUTPUT); //LED  
 dht.begin(); // 온습도센서 작동
}

void loop() {  
 // 온 습도 센서
 float air_humi = dht.readHumidity();
 float air_temp = dht.readTemperature();

 // 토양습도 1, 2
 soil_humi1 = analogRead(SOIL_HUMI1); 
 psoil_humi1 = map(soil_humi1, 1023, 0, 0, 100); 
 soil_humi2 = analogRead(SOIL_HUMI2); 
 psoil_humi2 = map(soil_humi2, 1023, 0, 0, 100); 
 // 물탱크 수위
 int tank_wlevel = analogRead(TANK_WATER); 

 // 조도 및 led
 val = analogRead(cds_pin); // A1에서 읽은 값을 val 변수에 저장
 ledval = map(val,0, 1023, 255, 0); // map함수를 사용하여 val값을 1~250으로 변환한 값을 ledval에 저장
 pledval = ledval*0.4; // 조도센서값을 0~100으로 표시하기 위한 설정


 // 초음파 센서 1
 float cycletime1;
 float distance1;
 digitalWrite(trig1, HIGH);
 delay(10);
 digitalWrite(trig1, LOW);
 cycletime1 = pulseIn(echo1, HIGH); 
 distance1 = ((340 * cycletime1) / 10000) / 2;  

 // 초음파 센서 2
 float cycletime2;
 float distance2;
 digitalWrite(trig2, HIGH);
 delay(10);
 digitalWrite(trig2, LOW);
 cycletime2 = pulseIn(echo2, HIGH); 
 distance2 = ((340 * cycletime2) / 10000) / 2; 

  StaticJsonDocument<200> sending_doc;
  sending_doc["air_humi"]  = air_humi;
  sending_doc["air_temp"]  = air_temp;
  sending_doc["pledval"]  = pledval;
  sending_doc["psoil_humi1"]  = psoil_humi1;
  sending_doc["psoil_humi2"]  = psoil_humi2;
  sending_doc["tank_wlevel"]  = tank_wlevel;  
  sending_doc["distance1"]  = distance1;
  sending_doc["distance2"]  = distance2;
  
  serializeJson(sending_doc, Serial);
  Serial.println();

  if (Serial.available()) {
    StaticJsonDocument<200> recvDoc;
    DeserializationError error = deserializeJson(recvDoc, Serial);
   
    if (!error) {
      String ledCommand = recvDoc["led"];

      // Serial.println(servoCommand);
      if (ledCommand == "on") {
        digitalWrite(ledpin, HIGH); // LED 켜기
        }
      else {
        digitalWrite(ledpin, LOW); // LED 끄기
        }
      }    
    }
  delay(1000);
}