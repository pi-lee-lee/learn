#pragma once


#include "../player/player.h"
#include "./monster.h"


class monster_b : monster, character{

    public:
        monster_b(){};
        ~monster_b(){};
        virtual void get_damage(int _damage) override;
        virtual void attack(player target_player)override;
        virtual void attack_special(player target_player)override;
};


