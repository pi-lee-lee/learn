#include <iostream>
#include <io.h>
#include <fcntl.h>

using namespace std;

int main() {
    // 💡 1. 충돌을 일으키던 setlocale(".UTF-8")을 완전히 제거하거나 빈값으로 둡니다.
    // _O_U16TEXT를 쓸 때는 운영체제 고유의 와이드 변환 기준을 따르도록 지시해야 합니다.


    // 💡 2. 질문자님이 원하시는 wchar_t 와이드 문자열 정의
    wchar_t mk[] = L"한국어";

    // 💡 3. 콘솔 창구를 2바이트 UTF-16 전용 통로로 개방합니다.
    _setmode(_fileno(stdout), _O_U16TEXT);

    // 💡 4. 와이드 전역 통로를 통해 안정적으로 출력 실행
    wcout << mk<<endl;

    std::system("pause"); 
    return 0;
}
