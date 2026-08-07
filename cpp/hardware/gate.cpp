#include <iostream>
#include <cstdint>
#include <functional> 
#include <array>

using namespace std;

void filter(unsigned int &temp){
    temp = ((temp|(~temp+1)) >> 31) & 0x00000001;
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

unsigned int n_nand_32(unsigned int a, unsigned int b){
    return n_not_32(n_and_32(a,b));
}

unsigned int n_xor(unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    return a^b;
}

unsigned int n_xor_32(unsigned int a, unsigned int b){
    return n_or_32(n_and_32(a,n_not_32(b)), n_and_32(n_not_32(a),b));
}

unsigned int n_mux(unsigned int sel, unsigned int a, unsigned int b){
    filter(a);
    filter(b);
    filter(sel);
    return n_or(n_and(n_not(sel),a), n_and(sel,b));
}

unsigned int n_mux_32(unsigned int sel, unsigned int a, unsigned int b){
    if(sel == 1)
        sel = 0xffffffff;
    return n_or_32(n_and_32(n_not_32(sel),a), n_and_32(sel,b));
}

unsigned int n_way_32(unsigned int a){
    // a | (-a) 는 0이 아니면 최상위가 무조껀 1 즉 a가 0이 아니면 최상위 비트가 1 
    // 1>>31 칸 밀어서 끝으로 그리고 혹시몰라 다시 & 연산으로 걸러냄  
    return ((a|(~a+1)) >> 31) & 0x00000001;
}

void n_dmux(unsigned int sel, unsigned int in, unsigned int *des){
    filter(in);
    filter(sel);
    des[0] = n_and(n_not(sel),in);
    des[1] = n_and(sel,in);
}

unsigned int n_mux_4_way32(unsigned int sel, unsigned int a, unsigned int b, unsigned int c, unsigned int d){
    unsigned int is_a = n_not(sel ^ 0x00000000); // sel == 0 이면 1, 아니면 0
    unsigned int is_b = n_not(sel ^ 0x00000001);
    unsigned int is_c = n_not(sel ^ 0x00000002);
    unsigned int is_d = n_not(sel ^ 0x00000003);

    
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
            for(unsigned int j = 0x00000001 ; j > 0 ; j = j<<1){
                for(unsigned int k = 0x00000001; k > 0 ; k = k<<1){
                    unsigned int result = func(i, j, k);
                    cout<<i<<","<<j<<","<<k<<"="<< result << endl; // 출력: false
                }            
            }
        }
    }
}


// void test(function<void(unsigned int, unsigned int, unsigned int*)> func, unsigned int size) {
//     if (func) { 
//         unsigned int* temp = new unsigned int[size];
//         for(unsigned int i = 0 ; i < 2 ; i++){
//             for(unsigned int j = 0 ; j < 2 ; j++){
//                 for(unsigned int k = 0 ; k < size ; k++){
//                     *(temp+k) = 0;
//                 }
//                 func(i, j, temp);

//                 string result = to_string(temp[0])+','+to_string(temp[1]);
//                 cout<<i<<","<<j<<"="<< result << endl; // 출력: false
//             }
//         }
//         delete[] temp;
//     }
// }

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
    // test(n_dmux,2);


    int c = 0xffffffff >> 31;
    cout<<hex<<c<<endl;

    // cout<<hex<<"\n\n\n"<<"and_32"<<endl;
    // test(n_and_32);
    // cout<<"or_32"<<endl;
    // test(n_or_32);
    // cout<<"nand_32"<<endl;
    // test(n_nand_32);
    // cout<<"xor_32"<<endl;
    // test(n_xor_32);
    // cout<<"mux_32"<<endl;
    // test(n_mux_32);

}