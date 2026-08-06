#pragma once  

#include <cstdint>

class bank{
    private:
        static int64_t tototo;
        int safe;
        int64_t location[2];
        char* text;
        bank();
        bank(int64_t temp, int64_t x, int64_t y);
    public:
        bank(const bank& other) = default; 
        ~bank();
        static bank genbank();
        void user_conter(int64_t _in, int64_t _out);
        void print(void);
};


class bank2 : bank{

    
};

