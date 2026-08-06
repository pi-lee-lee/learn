#pragma once
#include <string>

using namespace std;

class myexception{
    private:
        int code;
        string message;

    public:
        myexception(int code, string message);
        int getCode();
        string getMessage();
};