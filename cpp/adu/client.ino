#include <SoftwareSerial.h>
#define DEBUG true

SoftwareSerial wifi(7, 8);
// SoftwareSerial 속도의 한계: 현재 코드에서 wifi.begin(9600)으로 설정되어 있습니다. 9600bps는 초당 약 960바이트만 전송할 수 있는 매우 느린 속도입니다. 
// 앞서 만든 JSON 데이터가 약 150바이트이므로, 이 속도로는 1초에 겨우 5~6번 전송하면 채널이 꽉 차서 밀리기 시작합니다.
// 원격 서버 설정
const String SERVER_IP = "192.168.0.29";
const String SERVER_PORT = "9991";

// 데이터 전송 및 재접속 타이머 설정 (밀리초)
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 3000;    // 데이터양이 늘어났으므로 안정성을 위해 3초 주기로 변경

unsigned long lastConnectTime = 0;
const unsigned long connectInterval = 5000; 

bool isServerConnected = false;

void setup() {
  Serial.begin(115200);
  wifi.begin(9600); 

  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  wifi.print("AT+RST\r\n"); delay(2000);
  wifi.print("AT+CWMODE=1\r\n"); delay(1000); 
  wifi.print("AT+CWJAP=\"3F_302\",\"0424719222!!\"\r\n"); delay(5000);
  wifi.print("AT+CIPMUX=0\r\n"); delay(1000); 
  
  tryConnectToServer();

  while(wifi.available()) wifi.read();
  if (DEBUG) Serial.println("\n[PURE STREAM CLIENT READY] No-Blocking Mode Started.");
}

enum ParsingState { FIND_KEY, READ_VALUE };
ParsingState currentState = FIND_KEY;

String keyPattern = "\"pin\":"; 
int keyPatternIdx = 0;
int pinNumber = 0;

String closePattern = "CLOSED"; int closePatternIdx = 0;
String connectPattern = "CONNECT"; int connectPatternIdx = 0;
String alreadyPattern = "ALREADY CONNECTED"; int alreadyPatternIdx = 0;

void loop() {
  unsigned long currentMillis = millis();

  if (isServerConnected && (currentMillis - lastSendTime >= sendInterval)) {
    lastSendTime = currentMillis;
    sendJsonData();
  }

  if (!isServerConnected && (currentMillis - lastConnectTime >= connectInterval)) {
    lastConnectTime = currentMillis;
    tryConnectToServer();
  }

  while (wifi.available()) {
    char c = wifi.read(); 
    
    if (c == closePattern[closePatternIdx]) {
      closePatternIdx++;
      if (closePatternIdx == closePattern.length()) {
        isServerConnected = false;
        closePatternIdx = 0;
        if (DEBUG) Serial.println("\n[SERVER STATE] DISCONNECTED (CLOSED)");
      }
    } else { closePatternIdx = (c == closePattern[0]) ? 1 : 0; }

    if (c == connectPattern[connectPatternIdx]) {
      connectPatternIdx++;
      if (connectPatternIdx == connectPattern.length()) {
        isServerConnected = true;
        connectPatternIdx = 0;
        if (DEBUG) Serial.println("\n[SERVER STATE] CONNECTED SUCCESS");
      }
    } else { connectPatternIdx = (c == connectPattern[0]) ? 1 : 0; }

    // [수정 완료] 문자열 대신 첫 글자 캐릭터와 비교하도록 [0] 인덱스 추가
    if (c == alreadyPattern[alreadyPatternIdx]) {
      alreadyPatternIdx++;
      if (alreadyPatternIdx == alreadyPattern.length()) {
        isServerConnected = true;
        alreadyPatternIdx = 0;
        if (DEBUG) Serial.println("\n[SERVER STATE] ALREADY CONNECTED STATUS");
      }
    } else { alreadyPatternIdx = (c == alreadyPattern[0]) ? 1 : 0; } // <-- 수정됨

    switch (currentState) {
      case FIND_KEY:
        if (c == keyPattern[keyPatternIdx]) {
          keyPatternIdx++;
          if (keyPatternIdx == keyPattern.length()) {
            pinNumber = 0; keyPatternIdx = 0; currentState = READ_VALUE; 
          }
        } else { keyPatternIdx = (c == keyPattern[0]) ? 1 : 0; } // <-- 수정됨
        break;

      case READ_VALUE:
        if (c >= '0' && c <= '9') {
          pinNumber = (pinNumber * 10) + (c - '0');
        } 
        else if (c == ',' || c == ' ' || c == '\n' || c == '\r' || c == '}' || c == ']') {
          if (pinNumber > 0) {
            if (DEBUG) { Serial.print("\n[SERVER STREAM MATCHED] PIN: "); Serial.println(pinNumber); }
            pinMode(pinNumber, OUTPUT);
            digitalWrite(pinNumber, !digitalRead(pinNumber));
          }
          currentState = FIND_KEY; keyPatternIdx = 0;
        }
        break;
    }
  }
}


void tryConnectToServer() {
  if (DEBUG) Serial.println("\n[CONNECTING] Requesting connection to " + SERVER_IP + ":" + SERVER_PORT);
  wifi.print("AT+CIPSTART=\"TCP\",\"" + SERVER_IP + "\"," + SERVER_PORT + "\r\n");
}

// [핵심 수정] 가상 및 실제 센서 데이터를 모아서 한 번에 전송하는 대용량 JSON 빌더
void sendJsonData() {
  // 1. 센서 데이터 및 기기 상태 변수 수집
  String deviceId = "ARD_NODE_01";       // 장치 고유 ID
  unsigned long uptimeMs = millis();     // 아두이노 가동 시간 (밀리초)
  
  // 아날로그 센서 데이터 예시 (A0 ~ A3)
  int cdsValue = analogRead(A0);         // 조도 센서
  int gasValue = analogRead(A1);         // 가스/미세먼지 센서
  
  // 실수형(float) 데이터 예시 (가상 온습도 데이터 또는 실제 센서값 입력 가능)
  float temperature = 24.5 + (random(-5, 6) / 10.0); // 가상 온도 (24.0 ~ 25.0)
  int humidity = 60 + random(-2, 3);                 // 가상 습도 (58% ~ 62%)
  float vccVoltage = 4.95;                           // 아두이노 공급 전압 상태

  // 디지털 액추에이터 상태 수집
  int ledStatus = digitalRead(13);
  int relayStatus = digitalRead(12);     // 12번 핀에 릴레이가 있다고 가정

  // 2. 초경량 복합 구조 JSON 문자열 결합 (이스케이프 시퀀스 활용)
  String jsonPayload = "";
  jsonPayload += "{";
  jsonPayload += "\"device_id\":\"" + deviceId + "\",";
  jsonPayload += "\"uptime\":" + String(uptimeMs) + ",";
  jsonPayload += "\"vcc\":" + String(vccVoltage, 2) + ","; // 소수점 2자리까지
  jsonPayload += "\"sensors\":{";
  jsonPayload += "\"temp\":" + String(temperature, 1) + ","; // 소수점 1자리까지
  jsonPayload += "\"humi\":" + String(humidity) + ",";
  jsonPayload += "\"cds\":" + String(cdsValue) + ",";
  jsonPayload += "\"gas\":" + String(gasValue);
  jsonPayload += "},";
  jsonPayload += "\"status\":{";
  jsonPayload += "\"led\":" + String(ledStatus) + ",";
  jsonPayload += "\"relay\":" + String(relayStatus);
  jsonPayload += "}";
  jsonPayload += "}";

  // 3. AT 명령어를 통한 비블로킹 스트리밍 전송
  wifi.print("AT+CIPSEND=" + String(jsonPayload.length()) + "\r\n");
  
  // 데이터 길이가 늘어났으므로 하드웨어 송신 마진을 800us -> 1200us로 소폭 확보
  delayMicroseconds(1200); 
  
  wifi.print(jsonPayload);

  if (DEBUG) {
    Serial.print("[CLIENT SENT MULTI-JSON] (Length: ");
    Serial.print(jsonPayload.length());
    Serial.println(" Byte)");
    Serial.println(jsonPayload);
  }
}
