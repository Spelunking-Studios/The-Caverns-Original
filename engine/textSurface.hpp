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
        void setBgColor(sf::Color c);
        void moveTo(int x, int y);
        void render(void);
        std::vector<int> getSize(void);
    protected:
        int x, y, width, height;
        sf::Text *sfmlText;
        sf::Font *font;
        std::string text = "";
        sf::Color textColor = sf::Color::White;
        sf::Color bgColor = sf::Color::Black;
        void init(int x, int y, std::string text);
};

inline TextSurface::TextSurface(std::string text) : Surface(0, 0, 200, 100) {
    init(0, 0, text);
}

inline TextSurface::TextSurface(int x, int y, std::string text) : Surface(x, y, 200, 100) {
    init(x, y, text);
}

inline void TextSurface::init(int x, int y, std::string text) {
    this->text = text;
    // Create the font and load it
    font = new sf::Font();
    font->loadFromFile("assets/fonts/ComicSansMS.ttf");
    this->x = x;
    this->y = y;
    // Cause we need a SFML string (what?!?)
    sf::String string(this->text);
    // Create the SFML Text object
    sfmlText = new sf::Text(string, *font, 30u);
    // Apply half a million things to it
    sfmlText->setPosition(0, 0);
    sfmlText->setOrigin(0, 0);
    sfmlText->setScale(1, 1);
    sfmlText->setFillColor(textColor);
    // Make a float rect to define the size of the rendered text??
    sf::FloatRect textSize = sfmlText->getLocalBounds();
    textSize.height = sfmlText->getCharacterSize() + 5;
    textSize.width = sfmlText->findCharacterPos(this->text.size()).x - sfmlText->findCharacterPos(0).x;
    this->width = textSize.width;
    this->height = textSize.height;
    // Render
    render();
}

inline void TextSurface::moveTo(int x, int y) {
    this->x = x;
    this->y = y;
    render();
}

inline void TextSurface::render(void) {
    // Update the SFML Text to match the colors
    sfmlText->setFillColor(textColor);
    // A lot of annoying stuff to add the text to the surface
    // Create a render texture (so we can draw to it)
    sf::RenderTexture rt;
    // Create the render texture and set it up
    rt.create(width, height);
    rt.clear(this->bgColor);
    // Draw the text onto the render texture
    rt.draw(*sfmlText);
    // Call display because if we dont the whole thing goes wack.
    rt.display();
    // Make an actual texture from our render texture
    sf::Texture t = sf::Texture(rt.getTexture());
    // Resize ourself to fit the texture
    this->resize(width, height);
    this->Surface::init(this->x, this->y, (int)width, (int)height);
    // Load the texture into the surface??
    this->loadFromTexture(&t);
}

inline void TextSurface::setTextColor(sf::Color c) {
	this->textColor = c;
    this->init(this->x, this->y, this->text);
}

inline void TextSurface::setBgColor(sf::Color c) {
	this->bgColor = c;
    this->init(this->x, this->y, this->text);
}

inline std::vector<int> TextSurface::getSize(void) {
    return std::vector<int> {width, height};
}