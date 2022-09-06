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
        Surface();
        Surface(int x, int y, int width, int height);
        Surface(sf::FloatRect r);
        Surface(sf::IntRect r);
        ~Surface();
        sf::RenderWindow& operator>>(sf::RenderWindow& window);
        Surface& operator>>(Surface& s);
        sf::Image *image;
        int x, y, width, height;
        sf::Color fillColor = sf::Color(0, 0, 0, 255);
        void clear(void);
        void setFillColor(sf::Color c);
        void fill(void);
        void loadFromTexture(sf::Texture *texture);
        void draw(Surface *s);
        void draw(sf::Image& im);
        sf::Color getPixel(int x, int y);
        void setPixel(int x, int y, sf::Color c);
        void resize(int width, int height);
    protected:
        unsigned int signature = 0x0;
        void init(int x, int y, int width, int height);
};

inline Surface::Surface() {
    init(0, 0, 200, 100);
}

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
    shape.setPosition(sf::Vector2f(x, y));
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
    fillColor = c;
}

inline void Surface::fill(void) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            image->setPixel(x, y, fillColor);
        }
    }
    image->createMaskFromColor(fillColor, sf::Uint8(255));
}

inline void Surface::loadFromTexture(sf::Texture *texture) {
    *image = texture->copyToImage();
}

inline void Surface::draw(Surface *s) {
    draw(*s->image);
}

inline void Surface::draw(sf::Image& im) {
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            int k = x + i;
            int l = y + j;
            sf::Vector2u s(0, 0);
            s = im.getSize();
            if (k < 0 || k > (s.x - 1) || l < 0 || l > (s.y - 1)) {
                std::cout << "!!! (" << k << ", " << l << ") for " << s.x << " x " << s.y << " and "
                    << width << " x " << height << " with " << x << ", " << y << std::endl;
                continue;
            }
            sf::Color sp = image->getPixel(i, j);
            sp.a = 255;
            im.setPixel(k, l, sp);
        }
    }
}

inline sf::Color Surface::getPixel(int x, int y) {
    return image->getPixel(x, y);
}

inline void Surface::setPixel(int x, int y, sf::Color c) {
    image->setPixel(x, y, c);
}

inline void Surface::resize(int width, int height) {
    init(this->x, this->y, width, height);
}

#endif