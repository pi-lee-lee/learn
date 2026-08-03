// CMakeProject1.cpp : 애플리케이션의 진입점을 정의합니다.
//

#include "CMakeProject1.h"
#include <io.h>
#include <fcntl.h>


using namespace std;

int main()
{
	wchar_t mk[] = L"한국어";
	
	_setmode(_fileno(stdout), _O_U16TEXT);



	wcout << mk << endl;
	return 0;
}
