#include <Wire.h> 
#include <DHT.h> // 온습도센서 라이브러리 
//#include <Servo.h> //Servo 라이브러리

#define DHTPIN 4 // 온습도센서 핀번호
#define DHTTYPE DHT11
#define SOIL_HUMI1 A0
#define A_1A 9 // 모터드라이버 A_1A 단자 연결 핀번호(워터모터1용)
#define A_1B 10 // 모터드라이버 A_1B 단자 연결 핀번호
#define A_2A 5 // 모터드라이버 (환풍미니모터용)
#define A_2B 6 // 모터드라이버 (환풍미니모터용)

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
 pinMode(A_2A, OUTPUT);
 pinMode(A_2B, OUTPUT);  
 digitalWrite(A_2A, LOW);
 digitalWrite(A_2B, LOW); 
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

 // moniter print
 Serial.println();
 Serial.print("===================================");
 Serial.println();
 Serial.print("화분 1 수분량: ");
 Serial.print(psoil_humi1);
 Serial.println();
 Serial.println();  
 Serial.print(" / 온도: ");
 Serial.print(air_humi);
 Serial.print("  습도: ");
 Serial.print(air_temp);
 Serial.print("식물과 거리: ");
 Serial.print(distance);
 Serial.println("cm");
 Serial.println();  

 if(psoil_humi1 < 20) { // 토양수분값이 20미만이면
  analogWrite(A_1A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
  digitalWrite(A_1B, LOW);
  delay(5000);
  Serial.println("화분1 물공급!");
  digitalWrite(A_1A, LOW); // 워터펌프 중단
  digitalWrite(A_1B, LOW);
  digitalWrite(A_2A, LOW); // 워터펌프가 동작하는 동안 미니모터는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
  digitalWrite(A_2B, LOW); 
  }
 else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
  digitalWrite(A_1A, LOW);
  digitalWrite(A_1B, LOW);
  } 
 delay(1000);
 
 if(air_humi > 60){
  //servo.write(90.0);
  analogWrite(A_2A, 200); // 값을 변화(0~255)시키면서 팬의 세기를 설정
  digitalWrite(A_2B, LOW);
  delay(10000); 
  digitalWrite(A_2A, LOW); // 값을 변화(0~255)시키면서 팬의 세기를 설정
  digitalWrite(A_2B, LOW);  
  digitalWrite(A_1A, LOW);
  digitalWrite(A_1B, LOW);
  digitalWrite(A_2A, LOW);
  digitalWrite(A_2B, LOW);
  }
 else{
  //servo.write(175.0); 
  digitalWrite(A_2A, LOW);
  digitalWrite(A_2B, LOW);
  }
 delay(2000); 
}
