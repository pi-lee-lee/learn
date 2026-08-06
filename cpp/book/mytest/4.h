#pragma once
#include <string>

using namespace std;

class quiz{
    private:
        int month;
        int day;
    public:
        quiz(int month, int day);
        void setMonth(int month);
        void setDay(int dya);
        string getfourseason();
};