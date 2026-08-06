#pragma once


#include "../player/player.h"
#include "./monster.h"


class monster_b : monster, character{

    public:
        monster_b(){};
        ~monster_b(){};
        void get_damage(int _damage) override;
        void attack(player target_player)override;
        void attack_special(player target_player)override;
};


