#include <PID_v1.h>

const int photores = A0; // Photo resistor input pin
const int pot = A1; // Potentiometer input pin
const int led = 9; // LED output pin

// Tuning parameters for PID controller
float Kp=0; //Initial Proportional Gain 
float Ki=10; //Initial Integral Gain 
float Kd=0; //Initial Differential Gain

// Variables for storing sensor readings and control values
double lightLevel; // Holds incoming light level
double Setpoint, Input, Output; // Variables for storing values

// Create the PID object
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT); // Set up PID Loop: Input is PV, Output is u(t), Setpoint is SP

// Sampling rate for PID loop
const int sampleRate = 1; // Variable that determines how fast our PID loop runs

// Communication setup
const long serialPing = 500; //This determines how often we ping our loop 
                             // Serial pingback interval in milliseconds
unsigned long now = 0; //This variable is used to keep track of time
                       // placehodler for current timestamp
unsigned long lastMessage = 0; //This keeps track of when our loop last 
                               //Timestamp of the last serial message

void setup()
{
    // Initialize sensor readings and setpoints
    lightLevel = analogRead(photores); //Read in light level
    Input = map(lightLevel, 0, 1024, 0, 255); //Change read scale to analog //out scale
    Setpoint = map(analogRead(pot), 0, 1024, 0, 255); //get our setpoint from our pot

    //Start a serial session 
    Serial.begin(9600); 

    // Enable PID loop
    myPID.SetMode(AUTOMATIC); //Turn on the PID loop

    // Set PID loop sample rate
    myPID.SetSampleTime(sampleRate); //Sets the sample rate 

    // Print initialization message
    Serial.println("Begin"); // Hello World!

    // Record initialization timestamp
    lastMessage = millis(); // timestamp
}

void loop()
{
    // Update setpoint and sensor readings
    Setpoint = map(analogRead(pot), 0, 1024, 0, 255); //Read our setpoint
    lightLevel = analogRead(photores); //Get the light level
    Input = map(lightLevel, 0, 900, 0, 255); //Map it to the right scale 

    //Run the PID loop
    myPID.Compute(); 

    // Adjust LED brightness based on PID output
    analogWrite(led, Output); //Write out the output from the PID loop
        //to our LED pin

    // Update current time
    now = millis(); //Keep track of time

    // Send data over serial at specified interval
    if(now - lastMessage > serialPing) 
    {   //If it has been long enough give us
        //some info on serial
        // this should execute less frequently
        // send a message back to the mother ship
        // Send sensor readings and PID output over serial
        Serial.print("Setpoint = "); 
        Serial.print(Setpoint); 
        Serial.print(" Input = "); 
        Serial.print(Input); 
        Serial.print(" Output = "); 
        Serial.print(Output); 
        Serial.print("\n");

        // Receive PID tuning parameters over serial and update if new values are received
        if (Serial.available() > 0) 
        { //If we sent the program a command deal 
            //with it
            for (int x = 0; x < 4; x++) 
            { 
                switch (x) 
                {
                    case 0:
                        Kp = Serial.parseFloat();   // Read Proportional Gain
                        break;
                    case 1:
                        Ki = Serial.parseFloat();   // Read Integral Gain
                        break;
                    case 2:
                        Kd = Serial.parseFloat();   // Read Differential Gain
                        break;
                    case 3:
                        for (int y = Serial.available(); y == 0; y--) 
                        {
                            Serial.read();          //Clear out any residual junk 
                        }
                        break; 
                }
            }

            // Print received PID tuning parameters
            Serial.print(" Kp,Ki,Kd = ");
            Serial.print(Kp);
            Serial.print(",");
            Serial.print(Ki);
            Serial.print(",");
            Serial.println(Kd); //Let us know what we just received 

            // Update PID controller with new tuning parameters
            myPID.SetTunings(Kp, Ki, Kd); //Set the PID gain constants
            //and start running 
        }

        //update the time stamp.
        lastMessage = now; 
    } 
}
