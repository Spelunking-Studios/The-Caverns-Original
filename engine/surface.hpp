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
        sf::Color fillColor = sf::Color(0, 0, 0, 255);
        void clear(void);
        void setFillColor(sf::Color c);
        void fill(void);
        void loadFromTexture(sf::Texture *texture);
        void draw(Surface *s);
        void draw(sf::Image& im);
        sf::Color getPixel(int x, int y);
        void setPixel(int x, int y, sf::Color c);
    protected:
        unsigned int signature = 0x0;
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
    std::cout << "width: " << width << " height: " << height << " x: " << x << " y: " << y << std::endl;
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    // Sign the object
    signature = 0x12345;
    setFillColor(sf::Color::Black);
    image = new sf::Image();
    image->create(width, height, sf::Color::Black);
    std::cout << "Image size: " << image->getSize().x << ", " << image->getSize().y << std::endl;
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
    std::cout << "fillcolor: rgba(" << (int)fillColor.r << "," << (int)fillColor.g << "," << (int)fillColor.b << "," << (int)fillColor.a << ") " << std::endl;
}

inline void Surface::fill(void) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            image->setPixel(x, y, fillColor);
        }
    }
    std::cout << "|FILL| fillcolor: rgba(" << (int)fillColor.r << "," << (int)fillColor.g << "," << (int)fillColor.b << "," << (int)fillColor.a << ") " << std::endl;
    image->createMaskFromColor(fillColor, sf::Uint8(255));
}

inline void Surface::loadFromTexture(sf::Texture *texture) {
    *image = texture->copyToImage();
    std::cout << "Image size: " << image->getSize().x << ", " << image->getSize().y << std::endl;
}

inline void Surface::draw(Surface *s) {
    draw(*s->image);
}

inline void Surface::draw(sf::Image& im) {
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            sf::Color sp = image->getPixel(i, j);
            //sf::Color dp = im.getPixel(x + i, y + j);
            sp.a = 255;
            im.setPixel(x + i, y + j, sp);
        }
    }
}

inline sf::Color Surface::getPixel(int x, int y) {
    return image->getPixel(x, y);
}

inline void Surface::setPixel(int x, int y, sf::Color c) {
    image->setPixel(x, y, c);
}

#endif