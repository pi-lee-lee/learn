#include <SoftwareSerial.h>
#define DEBUG true

SoftwareSerial wifi(7, 8);

void setup() {
  Serial.begin(115200);
  
  // SoftwareSerial 안정성을 위해 9600 레이트 유지
  wifi.begin(9600); 

  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  // 초기화 명령어 (이 시점만 동기식 대기)
  wifi.print("AT+RST\r\n"); delay(2000);
  wifi.print("AT+CWMODE=3\r\n"); delay(1000);
  wifi.print("AT+CWJAP=\"3F_302\",\"0424719222!!\"\r\n"); delay(5000);
  wifi.print("AT+CIPMUX=1\r\n"); delay(1000);
  wifi.print("AT+CIPSERVER=1,9000\r\n"); delay(1000);
  
  // SoftwareSerial 버퍼 초기화
  while(wifi.available()) wifi.read();

  if (DEBUG) Serial.println("\n[PURE STREAM SERVER READY] Port 9000 Open. No-Blocking Mode.");
}

// 오직 무한 스트림 분석에만 집중하는 초경량 상태 머신
enum ParsingState { FIND_KEY, READ_VALUE };
ParsingState currentState = FIND_KEY;

// 연결 ID(소켓 세션) 백그라운드 추적용 변수
int currentConnectionId = 0; 
int ipdStage = 0; 

// 스트림 파싱 매칭용 변수
String keyPattern = "pin:";
int keyPatternIdx = 0;
int pinNumber = 0;

void loop() {
  // 메인 루프는 절대 멈추지 않고(Delay 0), 문자가 들어오는 즉시 연산하고 지웁니다.
  while (wifi.available()) {
    char c = wifi.read(); 
    
    // 1. 스트림 속에 섞여 들어오는 데이터 패킷의 소켓 ID를 실시간으로 스캐닝 (응답용)
    if (c == '+') { ipdStage = 1; }
    else if (ipdStage == 1 && c == 'I') { ipdStage = 2; }
    else if (ipdStage == 2 && c == 'P') { ipdStage = 3; }
    else if (ipdStage == 3 && c == 'D') { ipdStage = 4; }
    else if (ipdStage == 4 && c == ',') { ipdStage = 5; }
    else if (ipdStage == 5 && c >= '0' && c <= '9') {
      currentConnectionId = c - '0'; 
      ipdStage = 0;
    } else if (ipdStage > 0) {
      ipdStage = 0; 
    }

    // 2. 고속 스트림 파싱 엔진
    switch (currentState) {
      case FIND_KEY:
        if (c == keyPattern[keyPatternIdx]) {
          keyPatternIdx++;
          if (keyPatternIdx == keyPattern.length()) {
            pinNumber = 0;        
            keyPatternIdx = 0;    
            currentState = READ_VALUE; 
          }
        } else {
          // 패턴 매칭 실패 시 첫 글자('p')와 다시 대조하여 유연하게 인덱스 복귀
          keyPatternIdx = (c == keyPattern[0]) ? 1 : 0;
        }
        break;

      case READ_VALUE:
        if (c >= '0' && c <= '9') {
          pinNumber = (pinNumber * 10) + (c - '0');
        } 
        // 콤마(,)나 데이터 구분이 가능한 문자를 만나는 즉시 트리거
        else if (c == ',' || c == ' ' || c == '\n' || c == '\r' || c == '}') {
          if (pinNumber > 0) {
            if (DEBUG) {
              Serial.print("\n[STREAM MATCHED] PIN: ");
              Serial.println(pinNumber);
            }
            
            // 데이터 소비 즉시 제어 반영 (딜레이 없음)
            pinMode(pinNumber, OUTPUT);
            digitalWrite(pinNumber, !digitalRead(pinNumber));

            // [완전 비블로킹 응답 피드백] 
            // 와이파이 모듈의 응답을 기다리지 않고(확인용 targetKeyword 대기 루프 완전 삭제)
            // 하드웨어 버퍼에 쏠아버린 뒤 바로 다음 스트림 파싱으로 넘어갑니다.
            wifi.print("AT+CIPSEND=" + String(currentConnectionId) + ",7\r\n");
            delayMicroseconds(500); // AT 명령어 간 최소한의 하드웨어 전송 마진 (0.5밀리초)
            wifi.print("ACK:" + String(pinNumber) + "\n");
          }
          
          // 대기 시간 없이 곧바로 다음 "pin:" 키워드 스캐닝 상태로 완전 복귀
          currentState = FIND_KEY;
          keyPatternIdx = 0;
        }
        break;
    }
  }
}
