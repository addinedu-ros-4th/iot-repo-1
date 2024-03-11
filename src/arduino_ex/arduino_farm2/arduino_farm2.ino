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
 float distance;
 digitalWrite(trig2, HIGH);
 delay(10);
 digitalWrite(trig2, LOW);
 cycletime = pulseIn(echo2, HIGH); 
 distance = ((340 * cycletime) / 10000) / 2;  

 // 물탱크, 가습기 물 수위
 int tank = analogRead(TANK_WATER); 
 int humi = analogRead(HUMI_WATER);

 // moniter print
 Serial.println();
 Serial.print("===================================");
 Serial.println();
 Serial.print("화분 2 수분량: ");
 Serial.print(psoil_humi2); 
 Serial.println();
 Serial.println();
 Serial.print("조도: ");
 Serial.print(pledval);
 Serial.print("   식물과 거리: ");
 Serial.print(distance);
 Serial.println("cm");
 Serial.print("물탱크 수위: ");
 Serial.print(tank);
 Serial.print("  가습기 수위: ");
 Serial.print(humi);
 Serial.println();

 if (pledval > 20) { // 조도센서값이 60이 넘으면
  analogWrite(ledpin, pledval);  // LED는 조도센서 값의 밝기로 켜라 
  } 
 else{  // 그 외 조도센서값이면 LED를 꺼라
  analogWrite(ledpin, LOW);    
  }
 
 if(psoil_humi2 < 20) { // 토양수분값이 20미만이면
  analogWrite(B_1A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
  digitalWrite(B_2B, LOW);
  delay(5000);
  Serial.println("화분2 물공급!"); 
  digitalWrite(B_1A, LOW); // 워터펌프 중단
  digitalWrite(B_2B, LOW);
  }
 else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
  digitalWrite(B_1A, LOW);
  digitalWrite(B_2B, LOW);
  } 

 delay(2000); 
}
