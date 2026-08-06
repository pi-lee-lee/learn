#include "./4.h"
#include "./myexception.h"

#include "iostream"


quiz::quiz(int m, int d) : month(m-1), day(d) {

    if(m < 0 || d < 0){
        throw out_of_range("워짤라구요");
    }

    if(m > 7){
        if( m%2 == 1 && day > 30){
            throw myexception(1, "날짜가 잘못되었어요");
        }
    }else{
        if(m== 2 && day > 28){
            throw myexception(1, "날짜가 잘못되었어요");
        }
        else if(m%2 == 0 && day > 30){
            throw myexception(1, "날짜가 잘못되었어요");
        }
    }
    
}

void quiz::setDay(int day){
    this->day = day;
}

void quiz::setMonth(int month){
    this->month = month;
}

string quiz::getfourseason(){
    switch ((this->month+3) / 3){
        case 0:
            return "겨울";
        case 1:
            return "봄";
        case 2:
            return "여름";
        case 3:
            return "가을";
        case 4: 
            if((month+1) % 3 == 0)
                return "겨울";
        default:
            throw out_of_range("에라에라");
            throw myexception(0,"입력하신 월/일은 해당하는 계절이 없습니다.");
    };
}