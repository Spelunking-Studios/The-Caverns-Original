#ifndef THE_CAVERNS_HPP
#define THE_CAVERNS_HPP

#include <iostream>
#include <engine.hpp>
#include <ui/menu.hpp>
#include <ui/menu/component.hpp>
#include <ui/menu/text.hpp>
#include <vector>

#include "game.hpp"

extern Engine *e;
extern Game *game;
extern Menu *mainMenu;
extern int screenWidth;
extern int screenHeight;

void buildMainMenu(void);

#endif