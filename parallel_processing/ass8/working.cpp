#include <avr/sleep.h>

// Define pin numbers
#define LED_PIN 6
#define SWITCH_1_PIN 8
#define SWITCH_2_PIN 7

// Define frequency limits
#define MIN_FREQUENCY 0.5
#define MAX_FREQUENCY 8.0

// Define timer constants
const unsigned long TIMER1_COUNT1 = 15625; // Corresponds to 1Hz frequency

// Global variables
volatile float frequency = 1.0; // Initial frequency
volatile bool switch1Pressed = false;
volatile bool switch2Pressed = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(SWITCH_1_PIN, INPUT_PULLUP);
  pinMode(SWITCH_2_PIN, INPUT_PULLUP);
  
  // Enable pin change interrupts
  PCICR     |= B00000101;  // selects port B and port D
  PCMSK0 |= B00000001; //Enables PCINT0 (PortB-D8)
  PCMSK2 |= B10000000; //Enables PCINT23 (PortD-D7)

  // Initialize Timer1
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0xFFFF - TIMER1_COUNT1; // Initialize timer count
  TCCR1B |= (1 << CS10); // Start Timer1 with no prescaler

  // Enable Timer1 overflow interrupt
  TIMSK1 |= (1 << TOIE1);

  // Enable interrupts
  sei();
}

void loop() {
  // Enter sleep mode
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  sleep_mode();
}

// Pin Change Interrupt for SWITCH_1_PIN
ISR(PCINT0_vect) 
{
  if (digitalRead(SWITCH_1_PIN) == LOW) 
  {
    switch1Pressed = true;
  }
}

// Pin Change Interrupt for SWITCH_2_PIN
ISR(PCINT2_vect) 
{
  if (digitalRead(SWITCH_2_PIN) == LOW) 
  {
    switch2Pressed = true;
  }
}

// Timer1 overflow interrupt
ISR(TIMER1_OVF_vect) 
{
  // Increase the elapsed time since the last toggle
  static unsigned long previousToggleMillis = 0;
  unsigned long currentMillis = millis();
  unsigned long elapsedTime = currentMillis - previousToggleMillis;

  // Check if it's time to toggle the LED based on frequency
  if (elapsedTime >= (1000 / frequency)) 
  {
    toggleLED();
    previousToggleMillis = currentMillis;
  }

  // Adjust frequency if switches are pressed
  if (switch1Pressed) 
  {
    frequency /= 2;
    if (frequency < MIN_FREQUENCY) 
    {
        frequency = MIN_FREQUENCY;
    }
    updateTimer();

    switch1Pressed = false;
  }
  if (switch2Pressed) 
  {
    frequency *= 2;
    if (frequency > MAX_FREQUENCY) 
    {
        frequency = MAX_FREQUENCY;
    }
    updateTimer();
    switch2Pressed = false;
  }
}

// Function to toggle LED
void toggleLED() 
{
  static bool ledState = false;
  digitalWrite(LED_PIN, ledState);
  ledState = !ledState;
}

void updateTimer() 
{
  unsigned long newCount1 = TIMER1_COUNT1 * (1 / frequency);
  cli(); // Disable interrupts
  TCNT1 = 0xFFFF - newCount1; // Update Timer1 count
  sei(); // Enable interrupts
}