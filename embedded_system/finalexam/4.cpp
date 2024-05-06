/*
Write an Arduino program with bitmath style of coding that uses Timer 0 overflow (TIMER0_OVF_vect) to
generate a 100 Hz output signal at PIN 4. (Clock frequency = 16 MHz. For Normal Mode: WGMA = 000.
Counter value must be initialized to TCNT0. Set TOIE0 to enable timer overflow interrupt. Required
datasheet snapshots are given below).
*/
#include <avr/io.h>
#include <avr/interrupt.h>

const int outputPin = 4;  // Output pin connected to Pin 4

void setup() {
  pinMode(outputPin, OUTPUT);  // Set output pin as output

  // Configure Timer 0 for Normal Mode with prescaler 64
  TCCR0B |= (1 << CS01) | (1 << CS00);  // Set prescaler bits to 011 (64 prescaler)

  // Enable Timer 0 overflow interrupt
  TIMSK0 |= (1 << TOIE0);

  // Enable global interrupts
  sei();
}

void loop() {
  // No need for code in the loop since the interrupt handles the timer overflow
}

// Interrupt service routine for Timer 0 overflow
ISR(TIMER0_OVF_vect) {
  static int counter = 0;
  const int compareValue = 249;  // (16e6 / (64 * 100)) - 1, for 100 Hz frequency

  counter++;
  if (counter > compareValue) {
    digitalWrite(outputPin, !digitalRead(outputPin));  // Toggle the output pin
    counter = 0;  // Reset the counter
  }
}
