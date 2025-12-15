const int analogInPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int sensorValue = analogRead(analogInPin);

  // 数値だけを1行で送る
  Serial.println(sensorValue);

  // サンプリング周期（必要に応じて調整）
  // 例: 100Hz
  delay(10);
}