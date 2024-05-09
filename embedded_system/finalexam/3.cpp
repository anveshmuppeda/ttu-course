/*
Write an Arduino program with bitmath style of coding that uses interrupt PCINT0 (corresponding to PCIE0)
to toggle an LED connected to pin 13 (Port B) when a push switch connected to pin 8 (Port B) is pressed
(normally low). Set the microcontroller in deep sleep Power Save mode. (Required datasheet snapshots are
given below.)
*/
// Code 3
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/interrupt.h>

const int ledPin = 13;  // LED connected to Pin 13 (Port B)
const int switchPin = 8;  // Push switch connected to Pin 8 (Port B)

void setup() {
  pinMode(ledPin, OUTPUT);   // LED pin as output
  pinMode(switchPin, INPUT_PULLUP);  // Switch pin as input with pull-up resistor
  // Enable Pin Change Interrupt for Port B (PCINT0-7)
  PCICR |= (1 << PCIE0);
  // Enable Pin Change Interrupt for Pin 8 (PCINT0)
  PCMSK0 |= (1 << PCINT0);
  // Enable interrupts
  sei();
  // Set sleep mode to Power Save mode
  set_sleep_mode(SLEEP_MODE_PWR_SAVE);
}

void loop() {
  sleep_mode();  // Enter sleep mode
}

// Interrupt service routine for Pin Change Interrupt 0 (PCINT0)
ISR(PCINT0_vect) {
  // Check if the switch is pressed (LOW)
  if (digitalRead(switchPin) == LOW) {
    // Toggle the LED
    digitalWrite(ledPin, !digitalRead(ledPin));
    // Delay for debouncing (optional, depending on switch quality)
    delay(50);
  }
}

/*
Setup:
It defines that Pin 13 is connected to an LED, and Pin 8 is connected to a push button.
Configures Pin 13 as an output for the LED and Pin 8 as an input with a pull-up resistor for the button.
Enables Pin Change Interrupt (PCINT) for Port B (which includes Pin 8).
Sets the sleep mode to Power Save mode.
Loop:
It puts the microcontroller to sleep, waiting for an interrupt to wake it up.
Interrupt Service Routine (ISR):
When Pin 8 (the push button) changes state (e.g., pressed or released), it triggers the ISR.
Checks if the button is pressed (LOW state).
If pressed, toggles the LED on or off.
Includes a delay for debouncing (optional, used to handle switch bouncing issues).
So, when you press the button connected to Pin 8, it toggles the LED connected to Pin 13. The program stays in a low-power sleep mode until the button press interrupts it.
*/
