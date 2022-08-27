#include <iostream>
#include <SFML/Graphics.hpp>

class Window {
    public:
        // Constructor        
        Window();
        // Properties
        sf::RenderWindow* sfmlWindow;
};

inline Window::Window() {
    std::cout << "Creating window..." << std::endl;
    sfmlWindow = new sf::RenderWindow(sf::VideoMode(200, 200), "The Caverns");
}