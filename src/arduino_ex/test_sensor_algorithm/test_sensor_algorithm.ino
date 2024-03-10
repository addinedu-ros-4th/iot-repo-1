#include <Wire.h> 
#include <DHT.h> // 온습도센서를 사용하기 위한 라이브러리 추가
#include<Servo.h> //Servo 라이브러리를 추가
#define DHTPIN 4 // 온습도센서 데이터단자 연결 핀번호
#define DHTTYPE DHT11 // DHT11 센서일 경우 DHT11 , DHT22 센서일 경우 DHT22
#define SOIL_HUMI1 A0
#define SOIL_HUMI2 A2
#define TANK_WATER A3
#define HUMI_WATER A4
#define A_1A 9 // 모터드라이버 A_1A 단자 연결 핀번호(워터모터1용)
#define A_1B 10 // 모터드라이버 A_1B 단자 연결 핀번호
#define A_2A 11 // 모터드라이버 A_1A 단자 연결 핀번호(워터모터1용)
#define A_2B 12 // 모터드라이버 A_1B 단자 연결 핀번호
#define B_1A 5 // 모터드라이버 A_1A 단자 연결 핀번호 (미니모터용)
#define B_1B 6 // 모터드라이버 A_1B 단자 연결 핀번호

DHT dht(DHTPIN, DHTTYPE); // 온습도센서 사용 설정

Servo servo;      //Servo 클래스로 servo객체 생성
int cds_pin = A1; // 조도센서에 사용할 핀번호
int echo = 8; // 초음파센서
int trig = 13; // 초음파센서
int soil1, psoil1;  // 수분센서 값을 사용하기 위한 변수 선언
int soil2, psoil2; 
int val, ledval, pledval; // 조도센서 값을 사용하기 위한 변수 선언
int ledpin=3; // LED에 사용할 핀번호

void setup() { 
 Serial.begin(9600); // 시리얼 모니터 사용
 Serial.println("스마트팜 START!"); //시리얼 모니터에 문자 출력
 pinMode(trig, OUTPUT);
 pinMode(echo, INPUT);
 dht.begin(); // 온습도센서 작동
 pinMode(ledpin, OUTPUT); //LED 
 pinMode(A_1A, OUTPUT); // 모터드라이브 출력모드
 pinMode(A_1B, OUTPUT);  
 digitalWrite(A_1A, LOW); // 모터드라이브 초기값은 끈 상태
 digitalWrite(A_1B, LOW);
 pinMode(A_2A, OUTPUT); // 모터드라이브 출력모드
 pinMode(A_2B, OUTPUT);  
 digitalWrite(A_2A, LOW); // 모터드라이브 초기값은 끈 상태
 digitalWrite(A_2B, LOW); 
 pinMode(B_1A, OUTPUT);
 pinMode(B_1B, OUTPUT);  
 digitalWrite(B_1A, LOW);
 digitalWrite(B_1B, LOW); 
 servo.attach(2);
}
void loop() {  
 // 온 습도 센서
 float h = dht.readHumidity(); // 습도 값을 읽어 h에 입력, 그 값은 실수임 (온습도센서는 소수점 2자리까지 나타내도록 제작되어 있음)
 float t = dht.readTemperature(); // 온도 값을 읽어 t에 입력
 
 // 토양 수분 센서
 // soil1
 soil1 = analogRead(SOIL_HUMI1); // A0에서 읽은 값을 soil 변수에 저장
 psoil1 = map(soil1, 1023, 0, 0, 100); // map함수를 사용하여 soil값을 1~100으로 변환한 값을 psoil에 저장
 // soil2
 soil2 = analogRead(SOIL_HUMI2); // A3에서 읽은 값을 soil 변수에 저장
 psoil2 = map(soil2, 1023, 0, 0, 100); // map함수를 사용하여 soil값을 1~100으로 변환한 값을 psoil에 저장 
 // 조도 센서
 val = analogRead(cds_pin); // A1에서 읽은 값을 val 변수에 저장
 ledval = map(val,0, 1023, 255, 0); // map함수를 사용하여 val값을 1~250으로 변환한 값을 ledval에 저장
 pledval = ledval*0.4; // 조도센서값을 0~100으로 표시하기 위한 설정
 
 // 초음파 센서
 float cycletime;
 float distance;
 digitalWrite(trig, HIGH);
 delay(10);
 digitalWrite(trig, LOW);
 cycletime = pulseIn(echo, HIGH); 
 distance = ((340 * cycletime) / 10000) / 2;  

 // 물탱크, 가습기 물 수위
 int tank = analogRead(TANK_WATER); 
 int humi = analogRead(HUMI_WATER);

 // moniter print
 Serial.println();
 Serial.print("===================================");
 Serial.println();
 Serial.print("화분 1 수분량: ");
 Serial.print(psoil1);
 Serial.println();
 Serial.println();  
 Serial.print("화분 2 수분량: ");
 Serial.print(psoil2); 
 Serial.println();
 Serial.println();
 Serial.print("조도: ");
 Serial.print(pledval);
 Serial.print(" / 온도: ");
 Serial.print(t);
 Serial.print("  습도: ");
 Serial.print(h);
 Serial.println();  
 Serial.print("초음파와 거리: ");
 Serial.print(distance);
 Serial.println("cm");
 Serial.print("물탱크 수위: ");
 Serial.print(tank);
 Serial.print("  가습기 수위: ");
 Serial.print(humi);
 Serial.println();

 if (pledval > 60) { // 조도센서값이 60이 넘으면
  analogWrite(ledpin, pledval);  // LED는 조도센서 값의 밝기로 켜라 
 } 
  else{  // 그 외 조도센서값이면 LED를 꺼라
  analogWrite(ledpin, LOW);    
 }

if(psoil1 < 20) { // 토양수분값이 20미만이면
 analogWrite(A_1A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
 digitalWrite(A_1B, LOW);
 delay(5000);
 Serial.println("화분1 물공급!");
 digitalWrite(A_1A, LOW); // 워터펌프 중단
 digitalWrite(A_1B, LOW);
 digitalWrite(A_2A, LOW);
 digitalWrite(A_2B, LOW);
 digitalWrite(B_1A, LOW); // 워터펌프가 동작하는 동안 미니모터는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
 digitalWrite(B_1B, LOW); 
 }
 else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
 digitalWrite(A_1A, LOW);
 digitalWrite(A_1B, LOW);
} 
 delay(1000);
 
if(psoil2 < 20) { // 토양수분값이 20미만이면
 analogWrite(A_2A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
 digitalWrite(A_2B, LOW);
 delay(5000);
 Serial.println("화분2 물공급!"); 
 digitalWrite(A_2A, LOW); // 워터펌프 중단
 digitalWrite(A_2B, LOW);
 digitalWrite(A_1A, LOW);
 digitalWrite(A_1B, LOW);
 digitalWrite(B_1A, LOW); // 워터펌프가 동작하는 동안 미니모터는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
 digitalWrite(B_1B, LOW); 
 }
else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
 digitalWrite(A_2A, LOW);
 digitalWrite(A_2B, LOW);
} 
 delay(1000);

if(t >= 22 || h >= 70) { // 온도가 30이상 또는 습도가 80이상이면,  || => [Shift] + [\]
delay(5000);
 analogWrite(B_1A, 200); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);
 delay(5000);
 digitalWrite(B_1A, LOW); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);
 digitalWrite(A_1A, LOW);// 미니모터가 동작하는 동안 워터펌프는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
 digitalWrite(A_1B, LOW);
} 
else{ // 그 외 온습도 측정값이면 미니모터를 꺼라
 digitalWrite(B_1A, LOW);
 digitalWrite(B_1B, LOW);
}


if(h > 60){
 servo.write(90.0);
 analogWrite(B_1A, 200); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);
 delay(10000); 
 digitalWrite(B_1A, LOW); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);  
 digitalWrite(A_1A, LOW);
 digitalWrite(A_1B, LOW);
 digitalWrite(A_2A, LOW);
 digitalWrite(A_2B, LOW);
 }
else{
 servo.write(175.0); 
 digitalWrite(B_1A, LOW); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);     
}
 delay(2000); 
}
