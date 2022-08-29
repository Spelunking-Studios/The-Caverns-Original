#ifndef ENGINE_WINDOW_HPP
#define ENGINE_WINDOW_HPP

#include <iostream>
#include <SFML/Graphics.hpp>

class Window {
    public:
        Window(int width, int height);
        ~Window();
        int width, height;
        sf::RenderWindow* sfmlWindow;
};

inline Window::Window(int width, int height) {
    std::cout << "Creating window..." << std::endl;
    this->width = width;
    this->height = height;
    sfmlWindow = new sf::RenderWindow(sf::VideoMode(width, height), "The Caverns");
}

inline Window::~Window() {
    std::cout << "Closing window..." << std::endl;
    sfmlWindow->close();
}

#endif