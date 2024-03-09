#include <WiFi.h> //esp32에서 와이파이에 접속하기 위한 클래스

const char* ssid = "접속할 와이파이"; //접속 할 와이파이 이름
const char* password = "와이파이비번"; // 와이파이 비번
const char* host = "아이피주소"; // PC의 IP 주소, pc의 ip주소는 와이파이 바뀌면 바뀌니 터미널에서 ipconfig 를 쳐서 확인해야됨.
const int port = 8080; // PC의 포트 번호 // pc와 esp가 통신하기 위한 

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password); // 와이파이 연결
  
  while (WiFi.status() != WL_CONNECTED) { // 와이파이 연결 안되면 계속 ...찍는 코드
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP()); // 와이파이 연결되면 esp의 ip가 나옵니다.
}

void loop() {
  WiFiClient client; // esp에서 pc로 데이터를 보내기 위해 사용하는 클래스.

  if (!client.connect(host, port)) { //pc의 아이피 주소와 포트번호로 연결 시키고, 연결 되면 pc로 메세지를 보냅니다.
    Serial.println("Connection failed.");
    delay(5000);
  }
  else{
    Serial.println("Connected to server");
    client.println("Hello from ESP32!"); // PC로 메시지를 보냄
    delay(1000);
  }

  
}
