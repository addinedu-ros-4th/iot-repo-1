void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String received = Serial.readStringUntil('\n');
        Serial.print("Received: ");
        Serial.println(received);
    }
}
