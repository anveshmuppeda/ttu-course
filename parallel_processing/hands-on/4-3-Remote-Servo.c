#include <IRremote.hpp>
#include <Servo.h>
int IR_RECEIVE_PIN = 7;
int value;
Servo myservo; // create servo object
int pos = 0; // servo position

void setup() {
    Serial.begin(9600);
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
    myservo.attach(9); // attaches the servo on pin 9
}

void loop() {
    if (IrReceiver.decode()) {
        value = IrReceiver.decodedIRData.decodedRawData;
        //Serial.println( value, HEX); // Print "old" raw data
        /* USE NEW 3.x FUNCTIONS */
        //IrReceiver.printIRResultShort(&Serial); // Print complete received data in one line
        //IrReceiver.printIRSendUsage(&Serial); // Print the statement required to send this data
        switch(IrReceiver.decodedIRData.command) {
            case 0xX1: { 
            for(pos = 0; pos < 180; pos += 1) 
            { // forward
                myservo.write(pos);
                delay(50);
            }
            break;
            }
            case 0xX2: { 
            for(pos = 180; pos >= 1; pos -= 1) 
            { // forward
                myservo.write(pos);
                delay(50);
            }
            break;
            }
        }
        IrReceiver.resume(); // Enable receiving of the next value
    }
}