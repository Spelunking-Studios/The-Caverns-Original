#pragma once

#include <vector>
#include "../engine.hpp"
#include "menu/component.hpp"

class Menu {
    public:
        Menu(Engine *e);
        Engine *e;
        Surface *surface;
        std::vector<MenuComponent*> comps = {};
        int addComponent(MenuComponent *comp);
        void cycle(void);
};

inline Menu::Menu(Engine *e) {
    this->e = e;
    sf::Vector2u windowSize = this->e->window->sfmlWindow->getSize();
    //windowSize.y = 3;
    //windowSize.x = 3;
    surface = new Surface(0, 0, windowSize.x, windowSize.y);
    sf::Color c(0, 0, 0, 255);
    surface->setFillColor(c);
    surface->fill();
};

inline int Menu::addComponent(MenuComponent *comp) {
    this->comps.push_back(comp);
    return this->comps.size() - 1;
}

inline void Menu::cycle(void) {
    // Update all of the components
    for (int i = 0; i < comps.size(); i++) {
        comps[i]->update(e);
    }
    // Draw all of the components
    for (int i = 0; i < comps.size(); i++) {
        //std::cout << i << std::endl;
        //(*comps[i]) >> (*this->surface);
        comps[i]->draw(this->surface);
    }
    (*this->surface) >> *(e->window->sfmlWindow);
}