int relayPin = 8; // The pin to turn on the bulb
int pirPin = 7; // The pin to read the PIR sensor from
const int baud_rate = 9600; // Baud Rate for Serial Output
long waittime = (long)30; // Wait time for sensor warm up

/**
 * serialInput - Listens for serial input, and returns the integer value passed through it
 **/
int serialInput()
{
  while (!Serial.available());
  int value = Serial.parseInt();
  return value;
}

/**
 * pirInput - Reads, and returns, the digital value passed from the PIR sensor
 **/
int pirInput()
{
  int pirRead = digitalRead(pirPin);
  Serial.println(pirRead);
  return pirRead;
}

/**
 * callFunction - Calls the callback function passed in as a parameter, and writes it's resulting value to the `relayPin`
 *  @param callback - A function that returns an int and accepts no arguments
 **/
void callFunction(int (*callback)())
{
  int highOrNot = callback();
  digitalWrite(relayPin, highOrNot);
}

/**
 * setup - Arduino's setup function. Sets up the pins for I/O, as well as sets up Serial output.
 **/
void setup()
{
  pinMode(pirPin, INPUT);
  pinMode(relayPin, OUTPUT);
  Serial.begin(baud_rate);
  String wait_msg = "Wait " + String(waittime) + "sec before using the sensor";
  Serial.println(wait_msg);
  delay(waittime*1000);
}

/**
 * loop - Arduino's loop runction. Calls the requested "source" function that determines what turns the `relayPin` on and off
**/
void loop()
{
  callFunction(&pirInput);
}
