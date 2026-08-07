#include <iostream>
#include <vector>
#include <array>


using namespace std;


template<typename F> void setTestCallback(int a, F callback){
    callback(1,2,3,4);
}

template <typename T> T add (T a, T b){
    return a+b;
}

double add(double a, double b){
    cout<<"dldlslsdfl"<<endl;
    return a+b;
}

int main(int arg, char* argv[]){
    vector<int> vec;
    vector<double> ve1c;

    for(int i = 0; i < 10 ; i++){
        vec.push_back(i);
    }
    
    for(int i = 0; i < 10 ; i++){
        ve1c.push_back(1.0f+(double)i);
    }

    vector<int>::iterator it = vec.begin();
    vector<double>::iterator it2 = ve1c.begin();

    array<int,5> ar{1,2,3,4,5};
    
    setTestCallback(1, [](int a,int b,int c,int d){
        cout<<a<<b<<c<<d<<endl;
    });

    add(1.0, 1.0);

    return 0;
}


