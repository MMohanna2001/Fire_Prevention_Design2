#include <Servo.h>

Servo myservo;  // create servo object to control a servo
String x;
char t[80];
float vt;
// defines pins numbers
const int trigPin[] = {53,8,45,47};
const int echoPin[] = {51,9,43,49};
const char clos[] = { 'C', 'V', 'B', 'N'};
const char far[] = { 'F', 'G', 'H', 'I'};
// defines variables
long duration;
int distance;
const int timeoutDuration = 20000; // Timeout duration in microseconds
void setup() {
  for (int i = 0; i < 4; i++){
    pinMode(trigPin[i], OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin[i], INPUT); // Sets the echoPin as an Input  
  }
  pinMode(2,OUTPUT);
  
        digitalWrite(2,1);
  
  myservo.attach(7);  // attaches the servo on pin 9 to the servo object
  myservo.write(0); 
  Serial.begin(9600); // Starts the serial communication
  
}
void loop() {
    //digitalWrite(21,LOW);
    //delay(50);
    //digitalWrite(21,HIGH);
    //delay(50);
    for (int i = 0; i < 4; i++){
      // Clears the trigPin
      digitalWrite(trigPin[i], LOW);
      delayMicroseconds(2);
      // Sets the trigPin on HIGH state for 10 micro seconds
      digitalWrite(trigPin[i], HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin[i], LOW);
      // Reads the echoPin, returns the sound wave travel time in microseconds
      duration = pulseIn(echoPin[i], HIGH, timeoutDuration);
      // Calculating the distance
      // Check if timeout occurred
      distance = duration * 0.034 / 2;
      if (duration == 0) {
        // Handle timeout here (e.g., set distance to a default value)
        distance = 1000; // Set distance to -1 to indicate timeout
      }
        // Calculating the distance
      
      //Serial.println(distance);
      if (distance < 50){
        
        Serial.println(clos[i]);
      }else{
        Serial.println(far[i]);
      }
      delay(200);
    }
   
    
    if (Serial.available() > 0) {

    x = Serial.readString();
    x.toCharArray(t, 80);
    vt = atof(t);
    
    // Perform an action based on the received character
    if (vt == 2) {
       myservo.write(150); 
    } else if (vt == 1 || vt == 0 )  {
       myservo.write(0); 
      
       
    }
  }
    
    
}
