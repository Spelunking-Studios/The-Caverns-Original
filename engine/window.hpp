#include <iostream>
#include <SFML/Graphics.hpp>

class Window {
    public:
        // Constructor
        Window();
        ~Window();
        // Properties
        sf::RenderWindow* sfmlWindow;
};

inline Window::Window() {
    std::cout << "Creating window..." << std::endl;
    sfmlWindow = new sf::RenderWindow(sf::VideoMode(1200, 700), "The Caverns");
}

inline Window::~Window() {
    std::cout << "Closing window..." << std::endl;
    sfmlWindow->close();
}