#pragma once

#include "../character/character.h"
#include "../player/player.h"
#include "./monster.h"

class monster_a : monster, character{

    public:
        monster_a(){};
        ~monster_a(){};
        void get_damage(int _damage) override;
        void attack(player target_player)override;
        void attack_special(player target_player)override;
};


