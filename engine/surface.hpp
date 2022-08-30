#pragma once

#ifndef ENGINE_SURFACE_HPP
#define ENGINE_SURFACE_HPP

#include <SFML/Graphics/RectangleShape.hpp>
#include <SFML/Graphics/Texture.hpp>
#include <SFML/Graphics/Image.hpp>
#include <SFML/Graphics/RenderWindow.hpp>
#include <SFML/Graphics/Sprite.hpp>
#include <iostream>
#include <vector>

class Surface {
    public:
        Surface(int x, int y, int width, int height);
        Surface(sf::FloatRect r);
        Surface(sf::IntRect r);
        ~Surface();
        sf::RenderWindow& operator>>(sf::RenderWindow& window);
        Surface& operator>>(Surface& s);
        sf::Image *image;
        int x, y, width, height;
        void clear(void);
        void setFillColor(sf::Color c);
        void fill(void);
        void loadFromTexture(sf::Texture *texture);
        void draw(sf::Image& im);
    protected:
        unsigned int signature = 0x0;
        sf::Color *fillColor;
        void init(int x, int y, int width, int height);
};

inline Surface::Surface(int x, int y, int width, int height) {
    init(x, y, width, height);
}

inline Surface::Surface(sf::FloatRect r) {
    init(r.left, r.top, r.width, r.height);
}

inline Surface::Surface(sf::IntRect r) {
    init(r.left, r.top, r.width, r.height);
}

inline Surface::~Surface() {
    // Unsign the object
    signature = 0x0;
}

inline void Surface::init(int x, int y, int width, int height) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    // Sign the object
    signature = 0x12345;
    setFillColor(sf::Color::Black);
    image = new sf::Image();
    image->create(width, height, sf::Color::Black);
}

inline sf::RenderWindow& Surface::operator>>(sf::RenderWindow& window) {
    sf::Texture t;
    t.loadFromImage(*image);
    sf::RectangleShape shape;
    shape.setSize(sf::Vector2f(width, height));
    shape.setPosition(sf::Vector2f(0, 0));
    shape.setTexture(&t);
    window.draw(shape);
    return window;
}

inline Surface& Surface::operator>>(Surface& s) {
    s.draw(*image);
    return s;
}

inline void Surface::clear(void) {
    this->fill();
}

inline void Surface::setFillColor(sf::Color c) {
    fillColor = &c;
    std::cout << "fillcolor: rgba(" << (int)c.r << "," << (int)c.g << "," << (int)c.b << "," << (int)c.a << ") " << std::endl;
}

inline void Surface::fill(void) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            image->setPixel(x, y, *fillColor);
        }
    }
    image->createMaskFromColor(*fillColor, sf::Uint8(255));
}

inline void Surface::loadFromTexture(sf::Texture *texture) {
    *image = texture->copyToImage();
}

inline void Surface::draw(sf::Image& im) {
    *image = sf::Image(im);
}

#endif