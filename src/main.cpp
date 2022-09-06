#include "theCaverns.hpp"

void eventHandler(Engine *e, sf::Event event);
void mainLoop(Engine *e, sf::RenderWindow *window);
void gameLoop(Engine *e, sf::RenderWindow *window);

int screenWidth = 1200;
int screenHeight = 700;

Engine *e = new Engine(screenWidth, screenHeight);

int main(int argc, char**argv) {
    std::cout << "The Caverns" << std::endl;
    // Hook up the main loop and event handler
    (*e).setMainLoop(mainLoop);
    (*e).setEventHandler(eventHandler);
    (*e).setGameLoop(gameLoop);
    // Set the default background color of the window
    (*e).setClearColor(sf::Color::Green);
    // Build the meus
    buildMainMenu();
    // Start in a menu (the main menu)
    (*e).inMenu = true;
    // Run it
    (*e).run();
    return 0;
}

void eventHandler(Engine *e, sf::Event event) {
    // Handles all events
    if (event.type == sf::Event::Closed) {
        e->stop();
    }
    if (event.type == sf::Event::MouseButtonPressed) {
        e->setMouseButtonState(true);
    }
    if (event.type == sf::Event::MouseButtonReleased) {
        e->setMouseButtonState(false);
    }
}

void mainLoop(Engine *e, sf::RenderWindow *window) {
    // Runs every frame
    // Process events
    e->processEvents();
}

void gameLoop(Engine *e, sf::RenderWindow *window) {
    
}