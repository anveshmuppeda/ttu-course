/* Using bitmath technique, write an Arduino Uno code to light up 5 LEDs one by one when an analog light
sensor senses lesser lights progressively (arbitrary thresholds). The 5 LEDs are connected to digital pins 3 to
7. Ambient light sensor is connected to Analog Pin 0 (i.e., A0). Note: All 5 LEDs must be on when the
ambient light is at lowest (i.e., below the lowest threshold) and none of the LEDs must be on when the ambient
light is at highest (i.e., higher than the highest threshold). */
// Define the analog pin for the light sensor
const int lightSensorPin = A0;

// Define the digital pins for the LEDs
const int ledPins[] = {3, 4, 5, 6, 7};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

// Define thresholds for LED activation
const int thresholds[] = {50, 150, 300, 500, 800}; // Example thresholds, adjust as needed

void setup() {
  // Set LED pins as OUTPUT
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  // Read the analog value from the light sensor
  int lightValue = analogRead(lightSensorPin);
  
  // Convert the light value to LED states using bitmath
  int ledsOn = 0;
  for (int i = 0; i < numLeds; i++) {
    if (lightValue <= thresholds[i]) {
      ledsOn |= (1 << i); // Turn on ith bit
    }
  }

  // Turn on LEDs based on the bit pattern
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], bitRead(ledsOn, i));
  }
}
