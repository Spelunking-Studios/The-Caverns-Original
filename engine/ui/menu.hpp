#pragma once

#include <vector>
#include "../engine.hpp"

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
    //surface->setFillColor(sf::Color::Black);
    surface->fill();
    std::cout << "Menu created" << std::endl;
};

inline int Menu::addComponent(MenuComponent *comp) {
    this->comps.push_back(comp);
    return this->comps.size() - 1;
}

inline void Menu::cycle(void) {
    // Update all of the components
    for (int i = 0; i < comps.size(); i++) {
        comps[i]->update();
    }
    // Draw all of the components
    for (int i = 0; i < comps.size(); i++) {
        (*comps[i]) >> (*this->surface);
    }
    (*this->surface) >> *(e->window->sfmlWindow);
}