#include <iostream>


class Block;   // 전방 선언


class MyBase{
private:
    int key_;
    MyBase(int key):key_(key){
        std::cout
            << "MyBase 생성 : "
            << key_
            << "\n";
    }
public:
    class MyBaseFactory{
    private:
        // 외부 생성 금지
        MyBaseFactory(){
            std::cout<< "Factory 생성\n";
        }
        // Block만 Factory 생성 가능
        friend class Block;
    public:
        MyBase create(int key){
            return MyBase(key);
        }
    };
};

class Block{
private:
    MyBase base_;
public:
    Block():base_(MyBase::MyBaseFactory().create(100))
    {
        std::cout
            << "Block 생성\n";
    }
};




