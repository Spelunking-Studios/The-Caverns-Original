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
        void draw(Surface *s) override;
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
    sfmlText = new sf::Text(string, *font, 30u);
    sfmlText->setPosition(0, 0);
    sfmlText->setOrigin(0, 0);
    sfmlText->setScale(1, 1);
    // A lot of annoying stuff to add the text to the surface
    sf::RenderTexture rt;
    sf::FloatRect textSize = sfmlText->getLocalBounds();
    textSize.height = sfmlText->getCharacterSize();
    textSize.width = sfmlText->findCharacterPos(text.size()).x - sfmlText->findCharacterPos(0).x;
    std::cout << textSize.width << ", " << textSize.height << std::endl;
    rt.create(textSize.width, textSize.height);
    std::cout << rt.getSize().x << ", " << rt.getSize().y << std::endl;
    rt.clear(sf::Color::Transparent);
    rt.draw(*sfmlText);
    rt.display();
    sf::Texture t = sf::Texture(rt.getTexture());
    std::cout << t.getSize().x << ", " << t.getSize().y << std::endl;
    surface = new Surface(0, 0, textSize.width, textSize.height);
    surface->loadFromTexture(&t);
    std::cout << "Surface: " << surface->x << "," << surface->y << "," << surface->width << "," << surface->height << std::endl;
}

inline Surface& TextComponent::operator>>(Surface& s) {
    std::cout << ">>" << s.width << std::endl;
    *this->surface >> s;
    return s;
}

inline void TextComponent::draw(Surface *s) {
    surface->draw(s);
}