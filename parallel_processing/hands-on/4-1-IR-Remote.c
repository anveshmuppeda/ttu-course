#include <IRremote.hpp>
int IR_RECEIVE_PIN = 7;

void setup() 
{
    Serial.begin(9600);
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
}

void loop() 
{
    if (IrReceiver.decode()) 
    {
        Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
        // Print "old" raw data
        /* USE NEW 3.x FUNCTIONS */
        IrReceiver.printIRResultShort(&Serial);
        // Print complete received data in one line
        IrReceiver.printIRSendUsage(&Serial);
        // Print the statement required to send this data
        IrReceiver.resume(); // Enable receiving of the next value
    }
}