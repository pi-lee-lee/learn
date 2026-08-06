#include <iostream>

using namespace std;

class Console;

class User {

private:
    int count;
public:
    class Passkey {
        private:
            Passkey() {}
            friend class Console; 
    };

    User() : count(100) {}
    int getCount() const { return count; }

    void setCount(Passkey, int newCount) {
        this->count = newCount;
    }
};

class Console {
public:
    void userSetCount(User& user, int count) {
        user.setCount(User::Passkey(), count); 
    }
};

int main() {
    User p1;
    Console console;


    cout<<p1.getCount()<<endl;

    console.userSetCount(p1,1000);

//    p1.setCount(User::Passkey(),1000); 오류코드

    cout<<p1.getCount()<<endl;

    return 0;
}
