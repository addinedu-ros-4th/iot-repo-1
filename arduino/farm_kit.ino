#include <Wire.h> 
#include <LiquidCrystal_I2C.h> // LCD를 사용하기 위한 라이브러리 추가
#include <DHT.h> // 온습도센서를 사용하기 위한 라이브러리 추가
#define DHTPIN 4 // 온습도센서 데이터단자 연결 핀번호
#define DHTTYPE DHT11 // DHT11 센서일 경우 DHT11 , DHT22 센서일 경우 DHT22
#define A_1A 9 // 모터드라이버 A_1A 단자 연결 핀번호(워터모터용)
#define A_1B 10 // 모터드라이버 A_1B 단자 연결 핀번호
#define B_1A 5 // 모터드라이버 A_1A 단자 연결 핀번호 (미니모터용)
#define B_1B 6 // 모터드라이버 A_1B 단자 연결 핀번호
#define SOIL_HUMI A0

LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD I2C 통신 설정(주소, 글자수, 줄수)
DHT dht(DHTPIN, DHTTYPE); // 온습도센서 사용 설정

int cds_pin = A1; // 조도센서에 사용할 핀번호
int cds_ledpin=3; // LED에 사용할 핀번호
int soil, psoil;  // 수분센서 값을 사용하기 위한 변수 선언
int val, ledval, pledval; // 조도센서 값을 사용하기 위한 변수 선언

void setup() { 
 lcd.init(); // LCD 초기화
 lcd.clear(); // 이전에 출력한 값 지우기 
 lcd.backlight(); // 배경화면 빛이 들어오도록 설정 
 lcd.setCursor(0,0);  // 출력할 데이터의 위치, 첫 번째 칸, 첫 번째 줄 커서 이동
 lcd.print("SmartFarm Start!"); // 문자 출력
 lcd.setCursor (0,1); // 출력할 데이터의 위치, 첫 번째 칸, 두 번째 줄 커서 이동
 lcd.print("   - FUNKITLAB -  "); // 문자 출력, 이름은 수정하여 사용
 Serial.begin(9600); // 시리얼 모니터 사용
 Serial.println("스마트팜 START!"); //시리얼 모니터에 문자 출력
 delay(4000); // 4초간 지속
 dht.begin(); // 온습도센서 작동
 
 pinMode(A_1A, OUTPUT); // 모터드라이브 출력모드
 pinMode(A_1B, OUTPUT);  
 digitalWrite(A_1A, LOW); // 모터드라이브 초기값은 끈 상태
 digitalWrite(A_1B, LOW);
 pinMode(B_1A, OUTPUT);
 pinMode(B_1B, OUTPUT);  
 digitalWrite(B_1A, LOW);
 digitalWrite(B_1B, LOW);
 pinMode(cds_ledpin, OUTPUT);
}
void loop() {  
 float h = dht.readHumidity(); // 습도 값을 읽어 h에 입력, 그 값은 실수임 (온습도센서는 소수점 2자리까지 나타내도록 제작되어 있음)
 float t = dht.readTemperature(); // 온도 값을 읽어 t에 입력
//  if (isnan(h) || isnan(t)){ // 온습도센서 가 읽은 값이 숫자가 아니면
//   Serial.println("DHT센서 값 읽기 실패!"); // 문자 출력
//   return; //프로그램 종료
//   }
 soil = analogRead(SOIL_HUMI); // A0에서 읽은 값을 soil 변수에 저장
 psoil = map(soil, 1023, 0, 0, 100); // map함수를 사용하여 soil값을 1~100으로 변환한 값을 psoil에 저장
 val = analogRead(cds_pin); // A1에서 읽은 값을 val 변수에 저장
 ledval = map(val,0, 1023, 250, 0); // map함수를 사용하여 val값을 1~250으로 변환한 값을 ledval에 저장
 pledval = ledval*0.4; // 조도센서값을 0~100으로 표시하기 위한 설정
 lcd.init(); // LCD 초기화 
 lcd.clear(); // 이전에 출력한 값 지우기 
 lcd.backlight(); // 배경화면 빛이 들어오도록 설정 
 lcd.display(); // 내용을 표시
 lcd.setCursor(0,0);
 lcd.print("M: ");
 lcd.print(psoil);
 lcd.print("%");
 lcd.setCursor(8,0);
 lcd.print("D: ");
 lcd.print(pledval);  
 lcd.print("ph");
 lcd.setCursor(0,1);
 lcd.print("T: ");
 lcd.print(t,0);
 lcd.print("C");
 lcd.setCursor(8,1);
 lcd.print("H: ");
 lcd.print(h,0);  
 lcd.print("%");
 Serial.print("수분량: ");
 Serial.print(psoil);
 Serial.print("  조도: ");
 Serial.print(pledval);
 Serial.print("  온도: ");
  Serial.print(t);
  Serial.print("  습도: ");
  Serial.print(h);
  Serial.println();
  delay(1000); 

if(psoil < 20) { // 토양수분값이 20미만이면
 analogWrite(A_1A, 220); // 값을 변화(0~255)시키면서 호스에서 나오는 물의 양을 적정하게 설정
 digitalWrite(A_1B, LOW);
 delay(5000);
 digitalWrite(A_1A, LOW); // 워터펌프 중단
 digitalWrite(A_1B, LOW);
 digitalWrite(B_1A, LOW); // 워터펌프가 동작하는 동안 미니모터는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
 digitalWrite(B_1B, LOW);
 }
 else{  // 그 외 토양수분값이 측정되면 워터모터를 꺼라
 digitalWrite(A_1A, LOW);
 digitalWrite(A_1B, LOW);
} 
 delay(1000);
 
// if(t >= 22 || h >= 70) { // 온도가 30이상 또는 습도가 80이상이면,  || => [Shift] + [\]
// delay(5000);
 analogWrite(B_1A, 200); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);
 delay(5000);
 digitalWrite(B_1A, LOW); // 값을 변화(0~255)시키면서 팬의 세기를 설정
 digitalWrite(B_1B, LOW);
 digitalWrite(A_1A, LOW);// 미니모터가 동작하는 동안 워터펌프는 중지, 미니모터와 워터펌프가 동시 작동 시 전압 부족 현상 막음 
 digitalWrite(A_1B, LOW);
// } 
// else{ // 그 외 온습도 측정값이면 미니모터를 꺼라
//  digitalWrite(B_1A, LOW);
//  digitalWrite(B_1B, LOW);
// }
 delay(1000);
 
 if (pledval >20) { // 조도센서값이 60이 넘으면
  analogWrite(cds_ledpin, ledval);  // LED는 조도센서 값의 밝기로 켜라 
 } 
  else{  // 그 외 조도센서값이면 LED를 꺼라
  analogWrite(cds_ledpin, LOW);    
 }
}



// void setup() {
//   Serial.begin(9600); //시리얼 모니터를 시작합니다.
// }

// void loop() {
//   int level = analogRead(A0);  // 수분센서의 신호를 측정합니다.
//   Serial.println(level);   //시리얼 모니터에 값을 출력합니다.
// }
