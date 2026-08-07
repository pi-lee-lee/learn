#include <iostream>
#include <string>
#include <vector>
#include <array>


using namespace std;


template<typename F> void setTestCallback(int a, F callback){
    callback(1,2,3,4);
}

int main(int arg, char* argv[]){
    
    //콜빽람다.
    setTestCallback(1, [](int a,int b,int c,int d){
        cout<<a<<b<<c<<d<<endl;
    });
    
    
    //즉시수행 람다. 
    cout<<([](int a, int b, int c, int d)-> string{
        return to_string(a)+to_string(c)+to_string(b)+to_string(d);
    }(1,2,3,4))<<endl;
 
    return 0;
}