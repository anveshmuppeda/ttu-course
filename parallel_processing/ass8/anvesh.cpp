#include <avr/sleep.h>

// Defining the pin numbers
#define LED_PIN 6           // Pin connected to the LED
#define SWITCH_1_PIN 8      // Pin connected to the switch 1
#define SWITCH_2_PIN 7      // Pin connected to switch 2

// Defining the frequency limits
#define LOWEST_FREQUENCY 0.5        // Lowest limit of frequency (Hz)
#define HIGHEST_FREQUENCY 8.0       // Highest limit of frequency (Hz)

// Defining the timer constants
const unsigned long TIMER1_COUNT1 = 15625; // Corresponds to 1Hz frequency

// Global variables declaration
volatile float frequency = 1.0;                 // Initial frequency
volatile bool g_switchOnePressed = false;       // Flag for indicating if switch 1 is pressed
volatile bool g_switchTwoPressed = false;       // Flag for indicating if switch 2 is pressed

// Setup Function
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
    g_switchOnePressed = true;
  }
}

// Pin Change Interrupt for SWITCH_2_PIN
ISR(PCINT2_vect) 
{
  if (digitalRead(SWITCH_2_PIN) == LOW) 
  {
    g_switchTwoPressed = true;
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
  if (g_switchOnePressed) 
  {
    frequency /= 2;
    if (frequency < LOWEST_FREQUENCY) 
    {
        frequency = LOWEST_FREQUENCY;
    }
    updateTimer();

    g_switchOnePressed = false;
  }
  if (g_switchTwoPressed) 
  {
    frequency *= 2;
    if (frequency > HIGHEST_FREQUENCY) 
    {
        frequency = HIGHEST_FREQUENCY;
    }
    updateTimer();
    g_switchTwoPressed = false;
  }
}

// Function to toggle LED
void toggleLED() 
{
  static bool ledBulbState = false;
  digitalWrite(LED_PIN, ledBulbState);
  ledBulbState = !ledBulbState;
}

void updateTimer() 
{
  unsigned long updated_count = TIMER1_COUNT1 * (1 / frequency);
  cli(); // Disable interrupts
  TCNT1 = 0xFFFF - updated_count; // Update Timer1 count
  sei(); // Enable interrupts
}