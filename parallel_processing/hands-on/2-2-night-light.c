const int analogInPin = A0;
int sensorValue = 0;
void setup() {
    Serial.begin(9600);
    pinMode(7, OUTPUT);
}

void loop() {
    sensorValue = analogRead(analogInPin);
    Serial.print("Analog sensor value = ");
    Serial.println(sensorValue);

    if (sensorValue < 550) {
        digitalWrite(7, HIGH);
    } else {
        digitalWrite(7, LOW);
    }

    delay(100);
}