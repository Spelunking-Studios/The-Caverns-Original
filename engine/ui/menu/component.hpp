#pragma once

#include "../../engine.hpp"

class MenuComponent {
    public:
        MenuComponent();
        MenuComponent(Menu *menu);
    protected:
        Menu *menu;
};

inline MenuComponent::MenuComponent() {
    std::cout << "MenuComponent created" << std::endl;
}

inline MenuComponent::MenuComponent(Menu *menu) {
    this->menu = menu;
}