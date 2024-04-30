#include <avr/sleep.h>
// Defining pin numbers
// Pin connected to the LED
#define LED_PIN 6
// Pin connected to switch 1
#define SWITCH_1_PIN 8
// Pin connected to switch 2
#define SWITCH_2_PIN 7

// Defining frequency limits
// Low limit of frequency (Hz)
#define LOW_FREQUENCY 0.5
// High limit of frequency (Hz)
#define HIGH_FREQUENCY 8.0

// Defining timer constants
const unsigned long TIMER1_COUNT1 = 15625; // Corresponds to 1Hz frequency

// Declaration of Global variables
volatile float frequency = 1.0; // Initial frequency
// Flag indicating if switch 1 is pressed
volatile bool g_Switch1Pressed = false;
// Flag indicating if switch 2 is pressed
volatile bool g_Switch2Pressed = false;

// Function Setup
void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(SWITCH_1_PIN, INPUT_PULLUP);
  pinMode(SWITCH_2_PIN, INPUT_PULLUP);
  
  // Enable pin change interrupts
  // Selecting the port B and port D
  PCICR     |= B00000101; 
  // Enabling the PCINT0 (PortB-D8)      
  PCMSK0 |= B00000001;   
  // Enabling the PCINT23 (PortD-D7)       
  PCMSK2 |= B10000000;          

  // Initialize Timer1
  TCCR1A = 0;
  TCCR1B = 0;

  // Initializing the timer count to achieve 1Hz frequency
  TCNT1 = 0xFFFF - TIMER1_COUNT1; 
   // Starting the Timer1 with no prescaler
  TCCR1B |= (1 << CS10);

  // Enable Timer1 overflow interrupt
  TIMSK1 |= (1 << TOIE1);

  // Enable interrupts Globally
  sei();
}

// Loop function
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
    // Set flag indicating switch 1 is pressed
    g_Switch1Pressed = true; 
  }
}

// Pin Change Interrupt for SWITCH_2_PIN
ISR(PCINT2_vect) 
{
  if (digitalRead(SWITCH_2_PIN) == LOW) 
  {
    // Set flag indicating switch 2 is pressed
    g_Switch2Pressed = true;
  }
}

// Timer1 overflow interrupt
ISR(TIMER1_OVF_vect) 
{
  // Increase the elapsed time since the last toggle
  static unsigned long s_previousToggleMillis = 0;
  // Current time in milliseconds
  unsigned long currentMillis = millis();
  // Time elapsed since last toggle
  unsigned long elapsedTime = currentMillis - s_previousToggleMillis;

  // Check if it's time to toggle the LED based on frequency
  if (elapsedTime >= (1000 / frequency)) 
  {
    // Toggle the LED Func
    toggleLED();
    // Update last toggle time
    s_previousToggleMillis = currentMillis;
  }

  // Adjust frequency if switches are pressed
  if (g_Switch1Pressed) 
  {
    // Halve the frequency
    frequency /= 2;
    if (frequency < LOW_FREQUENCY) 
    {
        // Ensure frequency doesn't go below the lower limit
        frequency = LOW_FREQUENCY;
    }
    // Update Timer1 with the new frequency
    updateTimer();
    // Reset switch 1 flag
    g_Switch1Pressed = false;
  }
  if (g_Switch2Pressed) 
  {
    // Double the frequency
    frequency *= 2;
    if (frequency > HIGH_FREQUENCY) 
    {
        // Ensure frequency doesn't exceed the upper limit
        frequency = HIGH_FREQUENCY;
    }
    // Update Timer1 with the new frequency
    updateTimer();
    // Reset switch 2 flag
    g_Switch2Pressed = false;
  }
}

// Function to toggle LED
void toggleLED() 
{
  // Variable to store the current state of LED
  static bool s_ledState = false;
  // Toggle the LED state
  digitalWrite(LED_PIN, s_ledState);
  // Update LED state for next toggle
  s_ledState = !s_ledState;
}

// Function to update Timer1 based on the new frequency
void updateTimer() 
{
  // Calculate new timer count value
  unsigned long updatedCountOne = TIMER1_COUNT1 * (1 / frequency);
  // Disable the interrupts
  cli(); 
  // Updating the Timer1 count
  TCNT1 = 0xFFFF - updatedCountOne; 
  // Enable the interrupts
  sei(); 
}