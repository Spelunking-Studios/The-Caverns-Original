#ifndef ENGINE_WINDOW_HPP
#define ENGINE_WINDOW_HPP

#include <iostream>
#include <SFML/Graphics.hpp>
#include "surface.hpp"

class Window {
    public:
        Window(int width, int height);
        ~Window();
        int width, height;
        sf::RenderWindow* sfmlWindow;
        Surface *surface;
        void update(void);
};

inline Window::Window(int width, int height) {
    std::cout << "Creating window..." << std::endl;
    this->width = width;
    this->height = height;
    sfmlWindow = new sf::RenderWindow(sf::VideoMode(width, height), "The Caverns");
    // Center window
    sf::Vector2<int> wpos(sf::VideoMode::getDesktopMode().width / 2, sf::VideoMode::getDesktopMode().height / 2);
    wpos.x -= this->width / 2;
    wpos.y -= this->height / 2;
    sfmlWindow->setPosition(wpos);
    surface = new Surface(0, 0, width, height);
    surface->setFillColor(sf::Color::Black);
    surface->fill();
}

inline Window::~Window() {
    std::cout << "Closing window..." << std::endl;
    sfmlWindow->close();
}

inline void Window::update(void) {
    (*surface) >> (*sfmlWindow);
}

#endif