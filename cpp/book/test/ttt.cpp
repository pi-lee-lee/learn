#include <iostream>
#include <random>
#include <array>
#include <vector>
#include <map>
#include <list>
#include <deque>
#include <set>



using namespace std;


class MyClass {
public:
    void funcA() { std::cout << "A\n"; }
    void funcB() { std::cout << "B\n"; }
    void test(void);
    void test2(void);
};

void MyClass::test(void){
    vector<int> c;
    array<int, 10> a;
    list<int> l;
    deque<int> d;
    c = {1,2,3,4,5};
    for(int k : c){
        cout<<k<<endl;
    }
}

void MyClass::test2(void){
    set<int> s;
    multiset<int> ms;
    map<int,string> m;
    multimap<int,string> mm;
}


int main() {
    random_device rd;
    mt19937 gen(rd());
    unsigned long kk  = gen.operator()();
    double k = rd.entropy();

    cout << kk <<","<<k<< endl;
    uniform_int_distribution<int> dis(1, 6); // 1부터 10까지

    int random_value = dis(gen);
    // std::cout << random_value << std::endl;

    MyClass xcc;

    xcc.test();
    
    return 0;
}