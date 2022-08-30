#pragma once

#include "../../engine.hpp"

class MenuComponent {
    public:
        MenuComponent();
        MenuComponent(Menu *menu);
        void update(void) {};
        virtual Surface& operator>>(Surface& s);
    protected:
        Menu *menu;
};

inline MenuComponent::MenuComponent() {
    std::cout << "MenuComponent created" << std::endl;
}

inline MenuComponent::MenuComponent(Menu *menu) {
    this->menu = menu;
}

inline Surface& MenuComponent::operator>>(Surface& s) {
    return s;
}