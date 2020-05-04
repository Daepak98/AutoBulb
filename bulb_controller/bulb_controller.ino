int y = 0;
const int baud_rate = 9600;

void setup()
{
    Serial.begin(baud_rate);
}

void loop()
{
    Serial.print(y++);
    Serial.print("\n");
}
