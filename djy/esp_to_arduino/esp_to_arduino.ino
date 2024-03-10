void setup() {
  // 시리얼 통신 시작 (ESP32와 컴퓨터 간)
  Serial.begin(9600);
  Serial2.begin(9600);
}

void loop() {
  // ESP32에서 메시지를 보냄
  delay(10); // 1초 대기

  if (Serial.available()) {
    char val = Serial.read();
    Serial2.write(val);
  }
  if(Serial2.available()){
    char val = Serial2.read();
    Serial.write(val);
  }
}
