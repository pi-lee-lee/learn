#include <iostream>
#include <cstdint>
#include <io.h>
#include <fcntl.h>
using namespace std;
const long double km_per_mile = 1.609344;


int main(){
    
    short s;
    unsigned short us;
    int i;

    cout<<"char"<<'\t'<<sizeof(char)<<endl;
    cout<<"shot"<<'\t'<<sizeof(short)<<endl;
    cout<<"ushort"<<'\t'<<sizeof(unsigned short)<<endl;
    cout<<"int"<<'\t'<<sizeof(int)<<endl;
    cout<<"uint"<<'\t'<<sizeof(unsigned int)<<endl;
    cout<<"_int8_t"<<'\t'<<sizeof(int8_t)<<endl;
    cout<<"__int16"<<'\t'<<sizeof(int16_t)<<endl;
    cout<<"__int32"<<'\t'<<sizeof(int32_t)<<endl;
    cout<<"__int64"<<'\t'<<sizeof(int64_t)<<endl;
    cout<<"long"<<'\t'<<sizeof(long)<<endl;
    cout<<"ulong"<<'\t'<<sizeof(unsigned long)<<endl;
    cout<<"ll"<<'\t'<<sizeof(long long)<<endl;
    cout<<"ull"<<'\t'<<sizeof(unsigned long long)<<endl;


    string temp = "dkdkdk";
    
    cout<<temp<<endl;
    int ss = 0x80000000 ;
    cout<<ss<<endl;
    
    ss = ~ss;
    cout<<hex<<ss<<endl;
    
    ss -=1;
    cout<<hex<<ss<<endl;
    
    cout<<ss<<endl;
    cout<<dec;
    cout<<(2*2*2*2*2*2*2)<<endl;
    
    int *ptr = new int[100];

    for(int i = 0 ; i < 100; i++){
        *(ptr+i)= 100-i;
    }
    

    cout<<"ptrptr----------------------------------------------"<<endl;
    for(int i = 0 ; i< 100 ; i++){
        cout<<ptr[i]<<endl;
    }

    cout<<ptr<<endl;
    cout<<*(ptr+0)<<endl;
    cout<<*ptr+7<<','<<*(ptr+7)<<endl;

    delete[] ptr;


    int a =0 ;
    const int *pp = &a;

    int *const ppp = &a;

    int const pp2 = 1;

    int const &test = pp2;

    const int *ps =&a;

    cout<<pp<<endl;
    cout<<*pp<<endl;
    a= 7;
    cout<<pp<<endl;
    
    cout<<*pp<<endl;


    cout<<"한국어"<<endl;


    std::system("pause"); 
    return 0;
}