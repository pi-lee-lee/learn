#include <iostream>  
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

template<typename T, typename F> T filter(T list, F condition){
    T result;
    
    for(auto &item: list){
        if(condition(item)) inserter(result,result.end()) = item;
    }

    return result;
}

int main(int argc, char* argv[]) {

    vector<int> numbers = {2,7,1,8,3,6,4,5,9};

    vector<int> result = filter(numbers,[](int k)-> bool{
        if(k%2) return true;
        return false;
    });
    

    for(int zzz : result){
       cout<<zzz<<endl;
    }
 
    // for(int a: numbers){
    //     if(a%2==0){
    //         cout<<a<<":"<<"2n"<<endl;
    //     }
    // }

    return 0;
}
