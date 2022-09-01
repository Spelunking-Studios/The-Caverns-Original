/*
This class is meant to provide abstraction over the creation, updating, and rendering of text to the engine's internal Surface class.
*/

#pragma once

#include <SFML/Graphics/Text.hpp>
#include <SFML/Graphics/Font.hpp>
#include <SFML/Graphics/RenderTexture.hpp>
#include <SFML/Graphics/Texture.hpp>

#include "surface.hpp"

class TextSurface: public Surface {
    public:
        TextSurface(std::string text);
        TextSurface(int x, int y, std::string text);
        void setTextColor(sf::Color c);
    protected:
        int x, y;
        sf::Text *sfmlText;
        sf::Font *font;
        std::string text = "";
        sf::Color textColor = sf::Color::White;
        void init(int x, int y, std::string text);
};

inline TextSurface::TextSurface(std::string text) : Surface(0, 0, 200, 100) {
    init(0, 0, text);
}

inline TextSurface::TextSurface(int x, int y, std::string text) : Surface(x, y, 200, 100) {
    init(x, y, text);
}

inline void TextSurface::init(int x, int y, std::string text) {
    text = text;
    // Create the font and load it
    font = new sf::Font();
    font->loadFromFile("assets/fonts/ComicSansMS.ttf");
    // Cause we need a SFML string (what?!?)
    sf::String string(text);
    // Create the SFML Text object
    sfmlText = new sf::Text(string, *font, 30u);
    // Apply half a million things to it
    sfmlText->setPosition(0, 0);
    sfmlText->setOrigin(0, 0);
    sfmlText->setScale(1, 1);
    sfmlText->setFillColor(textColor);
    // A lot of annoying stuff to add the text to the surface
    // Create a render texture (so we can draw to it)
    sf::RenderTexture rt;
    // Make a float rect to define the size of the rendered text??
    sf::FloatRect textSize = sfmlText->getLocalBounds();
    textSize.height = sfmlText->getCharacterSize();
    textSize.width = sfmlText->findCharacterPos(text.size()).x - sfmlText->findCharacterPos(0).x;
    // Create the render texture and set it up
    rt.create(textSize.width, textSize.height);
    rt.clear(sf::Color::Transparent);
    // Draw the text onto the render texture
    rt.draw(*sfmlText);
    // Call display because if we dont the whole thing goes wack.
    rt.display();
    // Make an actual texture from our render texture
    sf::Texture t = sf::Texture(rt.getTexture());
    // Resize ourself to fit the texture
    this->resize(textSize.width, textSize.height);
    this->Surface::init(x, y, (int)textSize.width, (int)textSize.height);
    this->x = x;
    this->y = y;
    // Load the texture into the surface??
    this->loadFromTexture(&t);
}