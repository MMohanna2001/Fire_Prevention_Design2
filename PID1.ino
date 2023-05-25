#include <util/atomic.h> 
#define In1 7
#define In2 8
#define ENCA 2
#define ENCB 3
#define PWM 5
#define ENA A0
const int BUFFER_SIZE = 64;
char buffer[BUFFER_SIZE];
int index = 0;
String x;
char t[80];

//char buffer[20];

long prevT = 0;
int posPrev = 0;
volatile int pos_i = 0;
volatile float velocity_i = 0;
volatile long prevT_i = 0;

float v1Filt = 0;
float v1Prev = 0;
float v2Filt = 0;
float v2Prev = 0;

float eintegral = 0;
float edrivative = 0;
float preve = 0;
 
float vt = 0;

float kp = 1;
float ki = 0.15;



void setup() {
  Serial.begin(1152600);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(PWM,OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  digitalWrite(ENA,HIGH);  

  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);

  analogWrite(PWM,0);
      
  delay(5000);
   


}

void loop() {
  
  /*  measuring output speed */
      /*if (Serial.available()) {
    char receivedChar = Serial.read(); // Read the character from serial communication
    
       // Check for the delimiter
    if (receivedChar == ',') {
      buffer[index] = '\0';  // Null-terminate the string
      // Process the received data
      //Serial.println(buffer[1]);
      //Serial.println(buffer[0]);

      // Reset the buffer for the next data
      index = 0;
    } else {
      buffer[index] = receivedChar;
      index = (index + 1) % BUFFER_SIZE;  // Prevent buffer overflow
    }
    if (buffer[0] == 'S') {
      analogWrite(PWM,0);
    } else  {
      vt = float(buffer[1]);*/
  int pos = 0;
  float velocity2 = 0;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    pos = pos_i;
    velocity2 = velocity_i;}

  long currT = micros();
  float deltaT = ((float)(currT-prevT)) / 1.0e6;
  float velocity1 = (pos - posPrev) / deltaT;
  posPrev = pos;
  prevT = currT;
  
  float v1 = (velocity1/ 390) * 60;
  float v2 = (velocity2/ 390) * 60;

  v1Filt = 0.854 * v1Filt + 0.0728 * v1 + 0.0728 * v1Prev;
  v1Prev = v1;
  v2Filt = 0.854 * v2Filt + 0.0728 * v2 + 0.0728 * v2Prev;
  v2Prev = v2;
  
  Serial.println(v2Filt);
  

  /* reading input speed */
  //if (Serial.available() > 0){
  //  x = Serial.readString();
  //  x.toCharArray(t, 80);
  //  vt = atof(t);
  //}

    if (Serial.available() > 0) {
  char data = Serial.read();

  if (data == 'a') { // set motor direction and speed for 'a'
    vt = 0;
  } 
  else if (data == 'b') { // set motor direction and speed for 'b'
    vt = 50;
  }
  else if (data == 'c') { // set motor direction and speed for 'c'
    vt = 80;
  }
}
  
  /* applying control algorithm */
  float e = vt - v2Filt;
  eintegral = eintegral + e*deltaT;
  
  if( eintegral > 255/ki) {
    eintegral = 255/ki;
  }
  else if (eintegral < -255/ki){
    eintegral = -255/ki;
  }
  
  
  float u = kp * e + ki * eintegral ;
  preve = e;

  int dir = -1;
  if (u < 0)
    dir = 1;
  int pwr = (int) fabs(u);
  if (pwr > 255){
    pwr = 255;
  }
  if (vt == 0 ){
    pwr = 0;
  }
  
  setMotor(dir,pwr,PWM,In1,In2);
  
   
  
//}
  //    }
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){  
  analogWrite(PWM,pwmVal); // Motor speed
  if(dir == -1){ 
    // Turn one way
    digitalWrite(In1,HIGH);
    digitalWrite(In2,LOW);
  }
  else if(dir == 1){
    // Turn the other way
    digitalWrite(In1,LOW);
    digitalWrite(In2,HIGH);
  }
  else{
    // Or dont turn
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);    
  }
}

void readEncoder()
{
  int b = digitalRead(ENCB);
  int increment = 0;
  if (b > 0)
    increment = -1;
  else 
    increment = 1;

  pos_i = pos_i + increment;  

  long currT = micros();
  float deltaT = ((float)(currT - prevT_i)) / 1.0e6;
  velocity_i = increment / deltaT;
  prevT_i = currT;
}
