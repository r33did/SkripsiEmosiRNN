int count = 0;
void setup() {
  // put your setup code here, to run once:
   Serial.begin(74880);
}

void loop() {
  // put your main code here, to run repeatedly:
float pipi = analogRead(A0);
float alis = analogRead(A1);
//float volt = ((sensorValue/1024)*18000);
//  Serial.print("otot = ");
  Serial.println(str(pipi)+','+str(alis);
//  Serial.println(" mV");
}
