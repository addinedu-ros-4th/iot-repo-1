#include <ArduinoJson.h> //라이브러리 설치 필요
#include <Wire.h> 
#include <Servo.h> //Servo 라이브러리를 추가

#define SOIL_HUMI2 A2
#define TANK_WATER A3
#define HUMI_WATER A4
#define B_1A 11 // 모터드라이버 B_1A 단자 연결 핀번호(워터모터2용)
#define B_2B 12 // 모터드라이버 B_2B 단자 연결 핀번호


Servo servo;      //Servo 클래스로 servo객체 생성
int cds_pin = A1; // 조도센서에 사용할 핀번호
int echo2 = 8; // 초음파센서2
int trig2 = 13; // 초음파센서2
int soil_humi2, psoil_humi2; 
int val, ledval, pledval; // 조도센서 값을 사용하기 위한 변수 선언
int ledpin=3; // LED에 사용할 핀번호

void setup() { 
 Serial.begin(9600); // 시리얼 모니터 사용
 Serial.println("화분2 START!"); //시리얼 모니터에 문자 출력
 pinMode(trig2, OUTPUT);
 pinMode(echo2, INPUT);
 pinMode(ledpin, OUTPUT); //LED 
 pinMode(B_1A, OUTPUT); // 모터드라이브 출력모드
 pinMode(B_2B, OUTPUT);  
 digitalWrite(B_1A, LOW); // 모터드라이브 초기값은 끈 상태
 digitalWrite(B_2B, LOW); 
}
void loop() {  
 soil_humi2 = analogRead(SOIL_HUMI2); 
 psoil_humi2 = map(soil_humi2, 1023, 0, 0, 100);  
 // 조도 센서
 val = analogRead(cds_pin); // A1에서 읽은 값을 val 변수에 저장
 ledval = map(val,0, 1023, 255, 0); // map함수를 사용하여 val값을 1~250으로 변환한 값을 ledval에 저장
 pledval = ledval*0.4; // 조도센서값을 0~100으로 표시하기 위한 설정
 
 // 초음파 센서
 float cycletime;
 float distance2;
 digitalWrite(trig2, HIGH);
 delay(10);
 digitalWrite(trig2, LOW);
 cycletime = pulseIn(echo2, HIGH); 
 distance2 = ((340 * cycletime) / 10000) / 2;  

 // 물탱크, 가습기 물 수위
 int tank = analogRead(TANK_WATER); 
 int humi = analogRead(HUMI_WATER);

 // 보내는 센서값 (토양습도2, 거리2, 조도, 탱크수위, 가습기 수위)
 StaticJsonDocument<200> sending_doc;
 sending_doc["psoil_humi2"]  = psoil_humi2;
 sending_doc["distance2"]  = distance2;
 sending_doc["pledval"]  = pledval;
 sending_doc["tank_wlevel"]  = tank_wlevel;
 sending_doc["humi_wlevel"]  = humi_wlevel;  

 serializeJson(sending_doc, Serial);
 Serial.println();

 delay(100);
}
