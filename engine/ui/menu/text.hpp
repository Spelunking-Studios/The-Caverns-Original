#pragma once

#include "component.hpp"

class TextComponent: public MenuComponent {
    public:
        TextComponent(Menu *m, std::string text);
    protected:
        std::string text;
        Menu *menu;
};

inline TextComponent::TextComponent(Menu *m, std::string text) {
    this->menu = m;
    this->text = text;
}