#include <iostream>

using namespace std;

template <typename T = int>
class data_package{
    public:
        data_package(T first) :first(first) {}
        T print_out_ele();     
    private:
        T first;
};
template <typename T>
T data_package<T>::print_out_ele(){
    return first;
}

