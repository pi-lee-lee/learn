#pragma once


#include "../player/player.h"

class monster{ 
    public:
        virtual ~monster(){};
        virtual void get_damage(int _damage)=0;
        virtual void attack(player target_player)=0;
        virtual void attack_special(player target_player)=0;
};
