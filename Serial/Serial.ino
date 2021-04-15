int count = 0;
void setup() {
  // put your setup code here, to run once:
   Serial.begin(74880);
}

void loop() {
  // put your main code here, to run repeatedly:
  float pipi = analogRead(A1);
  float alis = analogRead(A2);
  Serial.print(pipi);
  Serial.print(',');
  Serial.println(alis);
}
