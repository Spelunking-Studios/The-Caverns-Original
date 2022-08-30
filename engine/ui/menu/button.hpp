#pragma once

#include "component.hpp"
#include "text.hpp"
#include "../../surface.hpp"

class ButtonComponent: public MenuComponent {
    public:
        ButtonComponent(Menu *m, std::string text);
        Menu *menu;
        TextComponent *textComp;
        Surface *surface;
        std::string *text;
        int x, y, width, height;
};

inline ButtonComponent::ButtonComponent(Menu *m, std::string text) : menu(m), text(&text) {
    x = 0;
    y = 0;
    width = 100;
    height = 50;
    surface = new Surface(x, y, width, height);
    textComp = new TextComponent(menu, text);
}