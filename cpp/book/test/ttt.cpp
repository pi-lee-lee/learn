#include <iostream>
#include <vector>

class MyClass {
public:
    void funcA() { std::cout << "A\n"; }
    void funcB() { std::cout << "B\n"; }
};

int main() {
    // 1. 각 함수를 가리킬 별개의 멤버 함수 포인터 선언
    void (MyClass::*ptrA)() = &MyClass::funcA;
    void (MyClass::*ptrB)() = &MyClass::funcB;

    // 2. 주소 출력을 위해 각각 캐스팅 (별개로 처리)
    void* rawPtrA = (void*&)(ptrA);
    void* rawPtrB = (void*&)(ptrB);

    // 완전히 다른 두 개의 주소가 출력됩니다.
    std::cout << "funcA 주소: " << rawPtrA << std::endl; // 예: 0x7ff704...
    std::cout << "funcB 주소: " << rawPtrB << std::endl; // 예: 0x7ff70c...
}