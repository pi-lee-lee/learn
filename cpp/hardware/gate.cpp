#include <iostream>
#include <cstdint>
#include <functional> 
#include <array>

using namespace std;

void filter(unsigned int &temp){
    temp = temp << 15;
    if(temp>1) temp = 1;
    if(temp<0) temp = 0;
}

unsigned int n_not(unsigned int a){
    filter(a);
    return !a;
}

unsigned int n_not_32(unsigned int a){
    return ~a;
}

unsigned int n_or(unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    return a|b;
}
unsigned int n_or_32(unsigned int a, unsigned int b){
    return a|b;
}

unsigned int n_and(unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    return a&b;
}

unsigned int n_and_32(unsigned int a, unsigned int b){
    return a&b;
}

unsigned int n_nand(unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    return n_not(n_and(a,b));
}

unsigned int n_xor(unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    return n_or(n_and(a,n_not(b)), n_and(n_not(a),b));
}

unsigned int n_mux(unsigned int sel, unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    filter(sel);
    return n_or(n_and(n_not(sel),a), n_and(sel,b));
}

void n_dmux(unsigned int sel, unsigned int in, unsigned int *des){
    filter(in);
    filter(sel);
    des[0] = n_and(n_not(sel),in);
    des[1] = n_and(sel,in);
}

void test(function<unsigned int(unsigned int, unsigned int)> func) {
    if (func) { 
        for(unsigned int i = 0 ; i < 2 ; i++){
            for(unsigned int j = 0 ; j < 2 ; j++){
                unsigned int result = func(i, j);
                cout<<i<<","<<j<<"="<< result << endl; // 출력: false
            }
        }
    }
}

void test(function<unsigned int(unsigned int, unsigned int, unsigned int)> func) {
    if (func) { 
        for(unsigned int i = 0 ; i < 2 ; i++){
            for(unsigned int j = 0 ; j < 2 ; j++){
                for(unsigned int k = 0; k< 2 ; k++){
                    unsigned int result = func(i, j, k);
                    cout<<i<<","<<j<<","<<k<<"="<< result << endl; // 출력: false
                }            
            }
        }
    }
}


void test(function<void(unsigned int, unsigned int, unsigned int*)> func, unsigned int size) {
    if (func) { 
        unsigned int* temp = new unsigned int[size];
        for(unsigned int i = 0 ; i < 2 ; i++){
            for(unsigned int j = 0 ; j < 2 ; j++){
                for(unsigned int k = 0 ; k < size ; k++){
                    *(temp+k) = 0;
                }
                func(i, j, temp);

                string result = to_string(temp[0])+','+to_string(temp[1]);
                cout<<i<<","<<j<<"="<< result << endl; // 출력: false
            }
        }
        delete[] temp;
    }
}

int main(){
    cout<<"and"<<endl;
    test(n_and);
    cout<<"or"<<endl;
    test(n_or);
    cout<<"nand"<<endl;
    test(n_nand);
    cout<<"xor"<<endl;
    test(n_xor);
    cout<<"mux"<<endl;
    test(n_mux);

    cout<<"dmux"<<endl;
    test(n_dmux,2);


    unsigned int k = 0xfffffffd;
    cout<<hex<<k<<endl;
    k = k<<31;
    k = k>>31;
    cout<<hex<< k << endl;
}