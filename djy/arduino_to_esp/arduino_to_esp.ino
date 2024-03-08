#include <SoftwareSerial.h>

// 소프트웨어 시리얼 객체 생성
SoftwareSerial soft(2, 3); // RX, TX 설정 (아두이노에 연결된 핀)

void setup() {
  Serial.begin(9600);
  soft.begin(9600);
}

void loop() {
  delay(10); // 1초 대기

  // 아두이노로부터 메시지를 읽음
  if (Serial.available()) {
    char val = Serial.read();
    soft.write(val);
  }
  if(soft.available()){
    char val = soft.read();
    Serial.write(val);
  }
}
