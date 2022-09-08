#pragma once

#include "../../engine.hpp"
#include "component.hpp"
#include "text.hpp"
#include "../../surface.hpp"
#include "../../textSurface.hpp"
#include "../../collision/collision.hpp"
#include "defaults.hpp"
#include <vector>

class ButtonComponent: public MenuComponent {
    public:
        ButtonComponent(Menu *m, std::string text);
        ButtonComponent(Menu *m, std::string text, int x, int y);
        ButtonComponent(Menu *m, std::string text, int x, int y, int width, int height);
        Menu *menu;
        Surface *surface;
        TextSurface *textSurface;
        std::string text;
        int x, y, width, height;
        bool clicked = false;
        sf::Color bgColor = sf::Color::White;
        sf::Color hoverBgColor = sf::Color::Yellow;
        sf::Color textColor = sf::Color::Black;
        void update(Engine *e) override;
        void draw(Surface *s) override;
        void setClickHandler(void (*ch)(void));
    protected:
        void init(Menu *m, int x, int y, int width, int height, std::string text);
        void (*clickHandler)(void);
};

inline ButtonComponent::ButtonComponent(Menu *m, std::string text) {
    init(m, 0, 0, 200, 50, text);
}

inline ButtonComponent::ButtonComponent(Menu *m, std::string text, int x, int y) {
    init(m, x, y, 200, 50, text);
}

inline ButtonComponent::ButtonComponent(Menu *m, std::string text, int x, int y, int width, int height) {
    init(m, x, y, width, height, text);
}

inline void ButtonComponent::init(Menu *m, int x, int y, int width, int height, std::string text) {
    // Set a bunch of variables
    menu = m;
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->text = text;
    // Create our textsurface
    textSurface = new TextSurface(0, 0, text);
    textSurface->setBgColor(bgColor);
    textSurface->setTextColor(textColor);
    textSurface->moveTo(
        ((width - textSurface->getSize()[0]) / 2),
        ((height - textSurface->getSize()[1]) / 2)
    );
    // Create our normal surface
    surface = new Surface(x, y, width, height);
    surface->setFillColor(bgColor);
    surface->fill();
    // Set the default click handler
    this->setClickHandler(_blankClickHandler);
}

inline void ButtonComponent::update(Engine *e) {
    RectCollider rc(x, y, width, height);
    // Hover
    bool on = rc.pointCollide(e->mousePosition.x, e->mousePosition.y);
    if (on) {
        surface->setFillColor(hoverBgColor);
        textSurface->setBgColor(hoverBgColor);
    } else {
        surface->setFillColor(bgColor);
        textSurface->setBgColor(bgColor);
    }
    surface->fill();
    // Click
    std::vector<int> c = e->getClick(0);
    if (c[0] > -1 && c[2] == 0) {
        clicked = rc.pointCollide(c[0], c[1]);
        if (clicked) {
            std::cout << "Clicked: " << c[0] << ", " << c[1] << std::endl;
            clickHandler();
        }
    }
    clicked = false;
}

inline void ButtonComponent::draw(Surface *s) {
    textSurface->draw(surface);
    surface->draw(s);
}

inline void ButtonComponent::setClickHandler(void (*ch)(void)) {
    this->clickHandler = ch;
}