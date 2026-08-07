#include <iostream>
#include <random>

using namespace std;


class MyClass {
public:
    void funcA() { std::cout << "A\n"; }
    void funcB() { std::cout << "B\n"; }
};


int main() {
    random_device rd;
    mt19937 gen(rd());
    unsigned long kk  = gen.operator()();
    double k = rd.entropy();

    cout << kk <<","<<k<< endl;
    uniform_int_distribution<int> dis(1, 6); // 1부터 10까지

    int random_value = dis(gen);
    std::cout << random_value << std::endl;
    return 0;
}