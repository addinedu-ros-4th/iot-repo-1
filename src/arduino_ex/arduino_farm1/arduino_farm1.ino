#include <ArduinoJson.h> //라이브러리 설치 필요
#include <Wire.h> 
#include <DHT.h> // 온습도센서 라이브러리 
//#include <Servo.h> //Servo 라이브러리

#define DHTPIN 4 // 온습도센서 핀번호
#define B_1A 5 // 모터드라이버 (환풍미니모터용)
#define B_1B 6 // 모터드라이버 (환풍미니모터용)
#define A_1A 9 // 모터드라이버 A_1A 단자 연결 핀번호(워터모터1용)
#define A_1B 10 // 모터드라이버 A_1B 단자 연결 핀번호
#define SOIL_HUMI1 A0
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE); // 온습도센서 사용 설정

//Servo servo1; // 환기 서보모터
// Servo servo2; // 가습 서보모터
int soil_humi1, psoil_humi1;
int echo1 = 8; // 초음파센서1
int trig1 = 13; // 초음파센서1

void setup() { 
 Serial.begin(9600); 
 Serial.println("화분1 START!"); //시리얼 모니터에 문자 출력
 pinMode(trig1, OUTPUT);
 pinMode(echo1, INPUT); 
 dht.begin(); // 온습도센서 작동
 pinMode(A_1A, OUTPUT); // 모터드라이브 출력모드
 pinMode(A_1B, OUTPUT);  
 digitalWrite(A_1A, LOW); // 모터드라이브 초기값은 끈 상태
 digitalWrite(A_1B, LOW);
 pinMode(B_1A, OUTPUT);
 pinMode(B_1B, OUTPUT);  
 digitalWrite(B_1A, LOW);
 digitalWrite(B_1B, LOW); 
 //servo.attach(1); // 환풍기 서보모터
 //servo.attach(2); // 가습기 서보모터
}

void loop() {  
 // 온 습도 센서
 float air_humi = dht.readHumidity();
 float air_temp = dht.readTemperature();
 soil_humi1 = analogRead(SOIL_HUMI1); 
 psoil_humi1 = map(soil_humi1, 1023, 0, 0, 100); 

 // 초음파 센서
 float cycletime;
 float distance;
 digitalWrite(trig1, HIGH);
 delay(10);
 digitalWrite(trig1, LOW);
 cycletime = pulseIn(echo1, HIGH); 
 distance = ((340 * cycletime) / 10000) / 2;  

  StaticJsonDocument<200> sending_doc;
  sending_doc["air_humi"]  = air_humi;
  sending_doc["air_temp"]  = air_temp;
  sending_doc["psoil_humi1"]  = psoil_humi1;
  sending_doc["distance"]  = distance;
  
  serializeJson(sending_doc, Serial);
  Serial.println();

  delay(100);

  // if (Serial.available()) {
  //   StaticJsonDocument<200> receiving_doc;
  //   DeserializationError error = deserializeJson(receving_doc, Serial);

  //   if (!error) {
  //   String ledCommand = recvDoc["led"];


  // }


}
