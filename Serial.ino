float sensorInput = A0;
float data;
float volt;
int n = 0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  data = analogRead(sensorInput);
  volt = ((data/1024)*18000);
  Serial.println(String(data)+";"+String(volt)+";"+String(n));
  n += 1;
  Serial.flush();
}
