#include <avr/interrupt.h>
#include <avr/sleep.h>
void setup () {
    cli(); // Disable global interrupt - atomic
    DDRB |= B100000; // Pin 13 output
    // Set timer 1 to normal mode
    TCCR1A = B00000000;
    // Set pre-scaler to 1024
    TCCR1B = B00000101;
    // Turn ON OVF
    TIMSK1 = B00000001;
    // Initial Timer1 value for 1 sec count
    TCNT1 = 0xC2F6;
    // Use an appropriate sleep mode
    set_sleep_mode(SLEEP_MODE_IDLE);
    sei(); // Enable global interrupt
}