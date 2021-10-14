void setup() {
  Serial.begin(9600);
}
int val = 0;
void loop() {
  if (Serial.available() > 0)
  {
    Serial.read();
    Serial.print("Val1:");
    val = analogRead(A0);
    Serial.print(val);
    Serial.print(":");
    val = analogRead(A1);
    Serial.print(val);
    Serial.println(":0");
  }
}
