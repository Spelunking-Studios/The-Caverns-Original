#include <iostream>
#include <engine.hpp>

void eventHandler(Engine *e, sf::Event event);
void mainLoop(Engine *e, sf::RenderWindow *window);

int main(int argc, char**argv) {
    std::cout << "The Caverns" << std::endl;
    Engine e;
    e.setMainLoop(mainLoop);
    e.setEventHandler(eventHandler);
    e.setClearColor(sf::Color::Green);
    e.run();
    return 0;
}

void eventHandler(Engine *e, sf::Event event) {
    if (event.type == sf::Event::Closed) {
        e->stop();
    }
}

void mainLoop(Engine *e, sf::RenderWindow *window) {
    // Clear the screen
    e->clearScreen();
    // Process events
    e->processEvents();
    // Update the screen
    e->window->sfmlWindow->display();
}