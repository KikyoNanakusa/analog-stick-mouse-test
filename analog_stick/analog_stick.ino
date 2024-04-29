// アナログスティックのピン定義
const int xPin = A0;
const int yPin = A1;
const int switchPin = A2;
const int touchPin = A5;

void setup() {
  // シリアル通信の開始
  Serial.begin(9600);
}

void loop() {
  // アナログスティックからの読み取り
  int xValue = analogRead(xPin);
  int yValue = analogRead(yPin);
  int switchValue = analogRead(switchPin);
  int touchValue = analogRead(touchPin);

  // シリアル通信を通じてPCに送信
  Serial.print(xValue);
  Serial.print(",");
  Serial.print(yValue);
  Serial.print(",");
  Serial.print(switchValue);
  Serial.print(",");
  Serial.println(touchValue);
  

  // ディレイ
  delay(10);
}
