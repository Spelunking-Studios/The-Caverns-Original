#pragma once

#include "../../engine.hpp"

class MenuComponent {
    public:
        MenuComponent();
        MenuComponent(Menu *menu, int x, int y);
        void update(void) {};
        virtual Surface& operator>>(Surface& s);
        virtual void draw(Surface *s);
        int x = 0;
        int y = 0;
    protected:
        Menu *menu;
};

inline MenuComponent::MenuComponent() {
    std::cout << "MenuComponent created" << std::endl;
}

inline MenuComponent::MenuComponent(Menu *menu, int x, int y) {
    this->menu = menu;
    this->x = x;
    this->y = y;
}

inline Surface& MenuComponent::operator>>(Surface& s) {
    std::cout << "blank" << std::endl;
    return s;
}

inline void MenuComponent::draw(Surface *s) {
    std::cout << "blank" << std::endl;
}