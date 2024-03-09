#include <Wire.h> 
#include <DHT.h> // 온습도센서를 사용하기 위한 라이브러리 추가
#define DHTPIN 4 // 온습도센서 데이터단자 연결 핀번호
#define DHTTYPE DHT11 // DHT11 센서일 경우 DHT11 , DHT22 센서일 경우 DHT22
#define SOIL_HUMI1 A0
#define SOIL_HUMI2 A2
#define TANK_WATER A3
#define HUMI_WATER A4

DHT dht(DHTPIN, DHTTYPE); // 온습도센서 사용 설정

int cds_pin = A1; // 조도센서에 사용할 핀번호
int echo = 8; // 초음파센서
int trig = 12; // 초음파센서
int soil1, psoil1;  // 수분센서 값을 사용하기 위한 변수 선언
int soil2, psoil2; 
int val, ledval, pledval; // 조도센서 값을 사용하기 위한 변수 선언

void setup() { 
 Serial.begin(9600); // 시리얼 모니터 사용
 Serial.println("스마트팜 START!"); //시리얼 모니터에 문자 출력
 pinMode(trig, OUTPUT);
 pinMode(echo, INPUT);
 dht.begin(); // 온습도센서 작동
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
 ledval = map(val,0, 1023, 250, 0); // map함수를 사용하여 val값을 1~250으로 변환한 값을 ledval에 저장
 pledval = ledval*0.4; // 조도센서값을 0~100으로 표시하기 위한 설정
 
 // 초음파 센서
 float cycletime;
 float distance;
 digitalWrite(trig, HIGH);
 delay(10);
 digitalWrite(trig, LOW);
 cycletime = pulseIn(echo, HIGH); 
 distance = ((340 * cycletime) / 10000) / 2;  

 // 물탱크 물 수위
 int tank = analogRead(TANK_WATER); 
 int humi = analogRead(HUMI_WATER);


 Serial.print("화분 1 수분량: ");
 Serial.print(psoil1);
 Serial.print(" / 화분 2 수분량: ");
 Serial.print(psoil2); 
 Serial.print("  조도: ");
 Serial.print(pledval);
 Serial.print(" / 온도: ");
 Serial.print(t);
 Serial.print("  습도: ");
 Serial.print(h);
 Serial.println();  
 Serial.print("초음파와 거리: ");
 Serial.print(distance);
 Serial.println("cm");
 Serial.print("  물탱크 수위: ");
 Serial.print(tank);
 Serial.print("  가습기 수위: ");
 Serial.print(humi);
 Serial.println();
 Serial.println();
 delay(2000); 
 
}