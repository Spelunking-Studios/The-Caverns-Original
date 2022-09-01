#pragma once

#include "component.hpp"
#include "../../surface.hpp"
#include "../../textSurface.hpp"
#include <SFML/Graphics/Text.hpp>
#include <SFML/Graphics/Font.hpp>
#include <SFML/Graphics/RenderTexture.hpp>
#include <SFML/Graphics/Texture.hpp>

class TextComponent: public MenuComponent {
    public:
        TextComponent(Menu *m, std::string text);
        Surface& operator>>(Surface& s) override;
        sf::Color textColor = sf::Color::White;
        void draw(Surface *s) override;
        void setTextColor(sf::Color c);
    protected:
        TextSurface *surface;
        std::string text;
        Menu *menu;
};

inline TextComponent::TextComponent(Menu *m, std::string text) {
    //TextSurface ts("Test");
    menu = m;
    text = text;
    surface = new TextSurface(0, 0, text);
    /*text = text;
    font = new sf::Font();
    font->loadFromFile("assets/fonts/ComicSansMS.ttf");
    sf::String string(text);
    sfmlText = new sf::Text(string, *font, 30u);
    sfmlText->setPosition(0, 0);
    sfmlText->setOrigin(0, 0);
    sfmlText->setScale(1, 1);
    sfmlText->setFillColor(textColor);
    // A lot of annoying stuff to add the text to the surface
    sf::RenderTexture rt;
    sf::FloatRect textSize = sfmlText->getLocalBounds();
    textSize.height = sfmlText->getCharacterSize();
    textSize.width = sfmlText->findCharacterPos(text.size()).x - sfmlText->findCharacterPos(0).x;
    rt.create(textSize.width, textSize.height);
    rt.clear(sf::Color::Transparent);
    rt.draw(*sfmlText);
    rt.display();
    sf::Texture t = sf::Texture(rt.getTexture());
    surface = new Surface(0, 0, textSize.width, textSize.height);
    surface->loadFromTexture(&t);*/
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