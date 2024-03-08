const int LED_PIN = 13;

void setup() {
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        String received = Serial.readStringUntil('\n');
        Serial.print("Received: ");
        Serial.println(received);

        // "button_pressed" 메시지를 받으면 LED를 켭니다.
        if (received.equals("button_pressed")) {
            digitalWrite(LED_PIN, HIGH);
            Serial.println("LED on");
        }
    }
}
