#include <iostream>  

#include "./player/player.h"
#include "./monster/monster_a.h"
#include "./monster/monster_b.h"

using namespace std;

int main(int argc, char* argv[]) {
    cout<<"한글"<<endl;
    player pl;
    monster_a ff;
    monster_b bb;

    ff.attack(pl);
    bb.attack_special(pl);

    return 0;
}
