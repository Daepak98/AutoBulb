int relayPin = 8;
int pirPin = 7;
const int baud_rate = 9600;
int read = 0;
long waittime = (long) 20*1000;
int serialInput()
{
  while (!Serial.available()) {}
  int value = Serial.parseInt();
  return value;
}

int pirInput()
{
  int pirRead = digitalRead(pirPin);
  Serial.println(pirRead);
  return pirRead;
}

void callFunction(int (*callback)())
{
  int highOrNot = callback();
  digitalWrite(relayPin, highOrNot);
}

void setup()
{
  pinMode(pirPin, INPUT);
  pinMode(relayPin, OUTPUT);
  Serial.begin(baud_rate);
  Serial.println("Wait 20 sec before using the sensor");
  delay(waittime);
}

void loop()
{
  callFunction(&pirInput);
}
