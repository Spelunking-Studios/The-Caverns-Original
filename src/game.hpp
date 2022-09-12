#pragma once

#include <SFML/Graphics/RenderWindow.hpp>
#include <rapidjson/document.h>
#include <rapidjson/pointer.h>
#include <rapidjson/error/en.h>

#include <surface.hpp>
#include <camera.hpp>
#include <level.hpp>
#include <vector>

#include "theCaverns.hpp"

class Game {
    public:
        Game(Engine *e);
        Surface *surface;
        Camera *camera;
        bool loaded = false;
        void cycle(sf::RenderWindow *window);
        void draw(sf::RenderWindow *window);
        void load(void);
    protected:
        Engine *e;
        std::vector<Floor*> floors = {};
};