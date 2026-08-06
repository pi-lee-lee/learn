#include <iostream>

#include "./monster_b.h"

using namespace std;

void monster_b::get_damage(int _damage){
    cout<<"쳐맞음: -"<<_damage<<"hp"<<endl;
}

void monster_b::attack(player target_player){
    cout<<"b기본때림 : 10"<<endl;
}

// void monster_b::attack_special(player target_player){
//     cout<<"특수스킬로 때림 : 20"<<endl;
// }

void monster_b::attack_special(player target_player){
    cout<<"b특수스킬로 때림 : 20"<<endl;
}