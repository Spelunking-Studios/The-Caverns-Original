#pragma once

#include "component.hpp"
#include "../../surface.hpp"
#include <SFML/Graphics/Text.hpp>
#include <SFML/Graphics/Font.hpp>
#include <SFML/Graphics/RenderTexture.hpp>
#include <SFML/Graphics/Texture.hpp>

class TextComponent: public MenuComponent {
    public:
        TextComponent(Menu *m, std::string text);
        Surface& operator>>(Surface& s) override;
    protected:
        sf::Text *sfmlText;
        sf::Font *font;
        Surface *surface;
        std::string text;
        Menu *menu;
};

inline TextComponent::TextComponent(Menu *m, std::string text) {
    menu = m;
    text = text;
    font = new sf::Font();
    font->loadFromFile("assets/fonts/ComicSansMS.ttf");
    sf::String string(text);
    sfmlText = new sf::Text(string, *font, 5u);
    // A lot of annoying stuff to add the text to the surface
    sf::RenderTexture rt;
    sf::FloatRect textSize = sfmlText->getLocalBounds();
    rt.create(textSize.width, textSize.height);
    rt.clear(sf::Color::Transparent);
    rt.draw(*sfmlText);
    sf::Texture t = sf::Texture(rt.getTexture());
    surface = new Surface(textSize);
    surface->loadFromTexture(&t);
}

inline Surface& TextComponent::operator>>(Surface& s) {
    *this->surface >> s;
    return s;
}