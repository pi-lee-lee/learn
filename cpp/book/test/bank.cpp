#include "bank.h"

#include <iostream>

using namespace std;

int64_t bank::tototo = 0;

bank::~bank(){
    delete[] text;
}
bank::bank() : safe(1000), location{1,2} {
    text = new char[100];
    cout<<"none타입"<<endl;
}
bank::bank(int64_t temp, int64_t x, int64_t y) : safe(temp), location{x,y} {
    cout<<"3타입"<<endl;
}

void bank::user_conter(int64_t _in, int64_t _out){
    safe += _in;
    safe -= _out;
}

void bank::print(void){
    cout<<"잔고:"<<safe<<"원"<<endl;\
    cout<<"위치:"<<location[0]<<","<<location[1]<<endl;
}

bank bank::genbank(){
    bank temp = bank();
    return temp;
}


