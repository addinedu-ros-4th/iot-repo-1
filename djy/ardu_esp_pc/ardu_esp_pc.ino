#include <WiFi.h>

const char* ssid = "KT_GiGA_4A30";
const char* password = "*";
const char* host = "172.30.1.9"; // PC의 IP 주소
const int port = 8080; // PC의 포트 번호

void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial2.begin(9600);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    //Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;

  if (!client.connect(host, port)) {
    //Serial.println("Connection failed.");
    delay(5000);
  }
  else{
    //Serial.println("Connected to server");
    if (Serial.available()) {
      char val = Serial.read();
      Serial2.write(val);
      client.println(val);
    }
    if(Serial2.available()){
      char val = Serial2.read();
      Serial.write(val);
      client.println(val);
    }    
    delay(1000);
  }

  
}
