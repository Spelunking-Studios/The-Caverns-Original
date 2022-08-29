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
        ~Surface();
        void operator>>(sf::RenderWindow& window);
        sf::Image *image;
        int x, y, width, height;
        sf::Color *fillColor;
        void clear(void);
        void setFillColor(sf::Color c);
        void fill(void);
    protected:
        unsigned int signature = 0x0;
};

inline Surface::Surface(int x, int y, int width, int height) : width(width), height(height), x(x), y(y) {
    // Sign the object
    signature = 0x12345;
    setFillColor(sf::Color::Black);
    image = new sf::Image();
    image->create(width, height, sf::Color::Blue);
    //std::cout << "Surface : " << image->getSize().x << " x " << image->getSize().y << std::endl;
}

inline Surface::~Surface() {
    // Unsign the object
    signature = 0x0;
}

inline void Surface::operator>>(sf::RenderWindow& window) {
    sf::Texture t;
    t.loadFromImage(*image);
    sf::RectangleShape shape;
    shape.setSize(sf::Vector2f(width, height));
    shape.setPosition(sf::Vector2f(0, 0));
    shape.setTexture(&t);
    window.draw(shape);
}

inline void Surface::clear(void) {
    this->fill();
}

inline void Surface::setFillColor(sf::Color c) {
    fillColor = &c;
}

inline void Surface::fill(void) {
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            image->setPixel(x, y, sf::Color::Black);
        }
    }
}

#endif