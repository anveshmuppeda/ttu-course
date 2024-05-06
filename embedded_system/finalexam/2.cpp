/*Write an Arduino program for a night light, where an analog temperature sensor is connected to analog input
pin A0, and 2 LEDs are connected to a digital output pins 10 and 11. The analog sensor values are polled in
every 5 seconds and saved in a mutex buffer A or B, both of size 12 Bytes. If mutex buffer A is full, next data
will start to be stored in mutex buffer B, and vice versa. Also, if any of the mutex buffer is full, the
corresponding data is averaged. If the average value is above Threshold1, then the heater is ON, otherwise
the heater is OFF (represented by the LED connected to pin 10). If the average value is below Threshold2,
then the cooler is ON, otherwise the cooler is OFF (represented by the LED connected to pin 11). Also, for
debugging purpose, use the serial port (monitor) to send each data (Baud rate = 9600) to a computer.*/

#include <Arduino.h>

const int sensorPin = A0;
const int heaterPin = 10;
const int coolerPin = 11;
const int threshold1 = 75; // Adjust threshold values as needed
const int threshold2 = 25;
const int bufferSize = 12;

volatile byte mutex = 0;
volatile byte bufferA[bufferSize];
volatile byte bufferB[bufferSize];
volatile bool bufferFullA = false;
volatile bool bufferFullB = false;
volatile bool heaterState = false;
volatile bool coolerState = false;

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(heaterPin, OUTPUT);
  pinMode(coolerPin, OUTPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(sensorPin), readSensor, CHANGE);
}

void loop() {
  if (bufferFullA) {
    // Calculate average and check thresholds for buffer A
    float averageA = calculateAverage(bufferA);
    heaterState = averageA > threshold1;
    coolerState = averageA < threshold2;
    bufferFullA = false;
    printData(averageA);
    clearBuffer(bufferA);
  }
  
  if (bufferFullB) {
    // Calculate average and check thresholds for buffer B
    float averageB = calculateAverage(bufferB);
    heaterState = averageB > threshold1;
    coolerState = averageB < threshold2;
    bufferFullB = false;
    printData(averageB);
    clearBuffer(bufferB);
  }

  digitalWrite(heaterPin, heaterState);
  digitalWrite(coolerPin, coolerState);
  delay(5000); // Polling interval of 5 seconds
}

void readSensor() {
  byte reading = analogRead(sensorPin) / 4; // scale down to fit into a byte
  if (mutex == 0) {
    addData(bufferA, reading);
    if (isBufferFull(bufferA)) {
      bufferFullA = true;
      mutex = 1;
    }
  } else {
    addData(bufferB, reading);
    if (isBufferFull(bufferB)) {
      bufferFullB = true;
      mutex = 0;
    }
  }
}

void addData(volatile byte* buffer, byte data) {
  for (int i = 0; i < bufferSize; i++) {
    if (buffer[i] == 0) {
      buffer[i] = data;
      break;
    }
  }
}

bool isBufferFull(volatile byte* buffer) {
  for (int i = 0; i < bufferSize; i++) {
    if (buffer[i] == 0) {
      return false;
    }
  }
  return true;
}

void clearBuffer(volatile byte* buffer) {
  for (int i = 0; i < bufferSize; i++) {
    buffer[i] = 0;
  }
}

float calculateAverage(volatile byte* buffer) {
  float sum = 0;
  int count = 0;
  for (int i = 0; i < bufferSize; i++) {
    if (buffer[i] != 0) {
      sum += buffer[i];
      count++;
    }
  }
  if (count > 0) {
    return sum / count;
  }
  return 0;
}

void printData(float average) {
  Serial.print("Average Temperature: ");
  Serial.print(average);
  Serial.println(" °C");
}
