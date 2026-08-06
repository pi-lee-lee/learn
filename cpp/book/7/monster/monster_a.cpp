#include "./monster_a.h"
#include <iostream>

using namespace std;

void monster_a::get_damage(int _damage){
    cout<<"쳐맞음: -"<<_damage<<"hp"<<endl;
}

void monster_a::attack(player target_player){
    cout<<"a기본때림 : 100"<<endl;
}

void monster_a::attack_special(player target_player){
    cout<<"a스킬로 때림 : 100"<<endl;
}