#include <iostream>

void print_func(){
    std::cout << "dkdk" << std::endl;
}


int input_func(void){
    int input_value;
    std::cin >> input_value;
    return input_value;
}

int main(int, char**){
    std::cout << "Hello, World!\n" ;
    
    print_func();
    // std::cout << input_func() <<std::endl;


    int int_value = 1;
    float float_value = 1.1f;

    void *ptr_value;

    ptr_value = &int_value;
    
    std::cout << ptr_value << std::endl;
    std::cout << *(int*)ptr_value << std::endl;

    ptr_value = &float_value;

    std::cout << ptr_value << std::endl;
    std::cout << *(float*)ptr_value << std::endl;

    for(char i = 32 ; i < 127 ; i++){
        std::cout << i << ((i % 16 == 0 ) ? '\n' : ',');
    }

    std::cout<<std::endl;

}


