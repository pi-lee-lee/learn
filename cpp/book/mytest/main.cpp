#include <iostream>
#include "./4.h"
#include "./myexception.h"


using namespace std;

void quiz1(){
    cout<<"구구단 "<<endl;

    for(int i = 2; i < 10 ; i++){
        cout<<i<<"단"<<endl;
        for(int j = 1 ; j < 10 ; j++){
            cout << i << "*"<<j <<"="<<(i*j)<<endl;
        }
    }
}

int inputMonth(){
    int month = -1 ;
    cin>>month;
    if(month < 1 || month > 12){
        return -1;
    }
    return month;
}

int inputDay(){
    int day = -1;
    cin>>day;
    if(day<1 || day>31)
        return -1;
    return day;
}

int main(int argc, char* argv[]){


    int m = inputMonth();
    int d = inputDay();

    cout<<m<<","<<d<<endl;
    
    try{
        quiz *ttt = new quiz(m,d);
        quiz q(m, d);
        cout<<q.getfourseason()<<endl;
        cout<<ttt->getfourseason()<<endl;
        delete ttt;
    }catch (myexception e){
        cout<<e.getMessage()<<endl;
    }catch (out_of_range e){
        cout<<e.what()<<endl;
    }

    
    return 0;
}

