#pragma once

#include "component.hpp"
#include "../../surface.hpp"
#include "../../textSurface.hpp"

class TextComponent: public MenuComponent {
    public:
        TextComponent(Menu *m, std::string text, int x, int y);
        Surface& operator>>(Surface& s) override;
        void draw(Surface *s) override;
        void setTextColor(sf::Color c);
	    void setBgColor(sf::Color c);
    protected:
        TextSurface *surface;
        std::string text;
        Menu *menu;
};

inline TextComponent::TextComponent(Menu *m, std::string text, int x, int y) {
    //TextSurface ts("Test");
    menu = m;
    text = text;
    surface = new TextSurface(x, y, text);
}

inline Surface& TextComponent::operator>>(Surface& s) {
    std::cout << ">>" << s.width << std::endl;
    *this->surface >> s;
    return s;
}

inline void TextComponent::draw(Surface *s) {
    surface->draw(s);
}

inline void TextComponent::setTextColor(sf::Color c) {
    surface->setTextColor(c);
}

inline void TextComponent::setBgColor(sf::Color c) {
	surface->setBgColor(c);
}
