#include <fstream> // 파일 입출력을 위해 상단에 추가
#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>

// 윈도우 소켓 라이브러리 링크 설정
#pragma comment(lib, "ws2_32.lib")

const int PORT = 9991;
const int BUFFER_SIZE = 1024;

int main() {
  // 1. 윈도우 소켓(Winsock) 초기화
  WSADATA wsaData;
  if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
    std::cerr << "Winsock 초기화 실패\n";
    return 1;
  }

  // 2. 서버 소켓 생성 (IPv4, TCP 프로토콜)
  SOCKET server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (server_socket == INVALID_SOCKET) {
    std::cerr << "소켓 생성 실패, 에러 코드: " << WSAGetLastError() << "\n";
    WSACleanup();
    return 1;
  }

  // 포트 재사용 옵션 설정
  char opt = 1;
  setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

  // 3. 주소 구조체 설정
  sockaddr_in server_addr{};
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = INADDR_ANY; // 모든 IP로부터의 접속 허용
  server_addr.sin_port = htons(PORT); // 호스트 바이트 순서를 네트워크 바이트 순서로 변경

  // 4. 소켓에 주소 할당 (Bind)
  if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
    std::cerr << "바인딩 실패, 에러 코드: " << WSAGetLastError() << "\n";
    closesocket(server_socket);
    WSACleanup();
    return 1;
  }

  // 5. 클라이언트 연결 대기 (Listen, 대기 큐 크기 5)
  if (listen(server_socket, 5) == SOCKET_ERROR) {
    std::cerr << "리스닝 실패, 에러 코드: " << WSAGetLastError() << "\n";
    closesocket(server_socket);
    WSACleanup();
    return 1;
  }

  std::cout << "윈도우 서버가 구동되었습니다. 포트: " << PORT << "\n";
  std::cout << "클라이언트 접속을 대기하는 중...\n";

  char buffer[BUFFER_SIZE];

  // [변경 핵심 1] 서버 메인 무한 루프 (서버 자체는 절대 종료되지 않음)
  while (true) {
    sockaddr_in client_addr{};
    int client_addr_len = sizeof(client_addr);
    
    // 6. 클라이언트 연결 수락 (Accept) - 새로운 클라이언트가 올 때까지 대기(Blocking)
    SOCKET client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);

    if (client_socket == INVALID_SOCKET) {
      std::cerr << "연결 수락 실패, 에러 코드: " << WSAGetLastError() << "\n";
      continue; // 서버를 종료하지 않고 다음 연결 대기로 넘어감
    }

    // 접속한 클라이언트 IP 확인
    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
    std::cout << "\n[CONNECTED] 클라이언트 접속 성공! IP: " << client_ip << "\n";

    // [변경 핵심 2] 현재 접속한 클라이언트와의 데이터 송수신 전용 루프
    while (true) {
      memset(buffer, 0, BUFFER_SIZE);

      // 데이터 수신
      int bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);
      
      if (bytes_received > 0) {
        std::cout << "[RECEIVED] 받은 JSON 데이터:\n" << buffer << "\n";

        // 파일 끝에 추가 모드로 기록
        std::ofstream file("data_log.json", std::ios::app);
        if (file.is_open()) {
          file << buffer << "\n"; 
          file.close();
          std::cout << "파일에 데이터 추가 완료!\n";
        } else {
          std::cerr << "파일을 열 수 없습니다.\n";
        }
      } 
      else if (bytes_received == 0) {
        // 아두이노가 접속을 끊었거나 재부팅된 경우
        std::cout << "[DISCONNECTED] 클라이언트가 접속을 종료했습니다.\n";
        break; // 현재 클라이언트 루프를 탈출하여 다음 accept로 이동
      } 
      else {
        // 통신 에러 발생 시 처리
        int error_code = WSAGetLastError();
        if (error_code != WSAECONNRESET) { 
          std::cerr << "수신 에러 발생, 에러 코드: " << error_code << "\n";
        } else {
          std::cout << "[DISCONNECTED] 클라이언트 연결이 강제로 끊겼습니다.\n";
        }
        break; // 현재 클라이언트 루프 탈출
      }
    }

    // 현재 핸들링하던 클라이언트 소켓 안전하게 정리 후 다음 클라이언트 대기
    closesocket(client_socket);
    std::cout << "다음 클라이언트 연결을 대기합니다...\n";
  }

  // 이 아래 코드는 도달하지 않지만 논리적 구조를 위해 유지
  closesocket(server_socket);
  WSACleanup();
  return 0;
}
