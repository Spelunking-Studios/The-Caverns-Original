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
    surface = new Surface(0, 0, width, height);
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