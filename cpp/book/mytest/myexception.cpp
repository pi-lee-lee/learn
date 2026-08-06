#include "./myexception.h"

myexception::myexception(int code, string msg) : code(code), message(msg) {}
int myexception::getCode(){return code;}
string myexception::getMessage(){return message;}