#pragma once

#include <iostream>
#include <vector>
#include <exception>

#include <SFML/System/Clock.hpp>
#include <SFML/System/Time.hpp>

class Menu;

#include "window.hpp"
#include "sprite.hpp"
#include "surface.hpp"
#include "exceptions.hpp"
#include "collision/collision.hpp"

class Engine {
    public:
        // Constructor & Destructor
        Engine();
        Engine(int width, int height);
        // Properties
        int width = 1;
        int height = 1;
        Window *window;
        Menu *activeMenu;
        bool inMenu = false;
        std::vector<Menu *> menus = {};
        void (*eventHandler)(Engine *e, sf::Event event);
        void (*mainLoopFn)(Engine *e, sf::RenderWindow *window);
        void (*gameLoopFn)(Engine *e, sf::RenderWindow *window);
        sf::Color clearColor = sf::Color::Black;
        sf::Clock *clock;
        unsigned int fps = 0;
        int deltaTime = 0;
        sf::Vector2i mousePosition = sf::Mouse::getPosition();
        // Methods
        void run(void);
        void stop(void);
        void setMainLoop(void (*fn)(Engine *e, sf::RenderWindow *window));
        void setGameLoop(void (*fn)(Engine *e, sf::RenderWindow *window));
        void setEventHandler(void (*callback)(Engine *e, sf::Event event));
        void processEvents(void);
        void clearScreen(void);
        void setClearColor(sf::Color c);
        int addMenu(Menu *m);
        void setMenu(int index);
        int clickAt(int x, int y, int button);
        std::vector<int> getClick(int index);
        void popClick(void);
        void setMouseButtonState(bool s, sf::Mouse::Button b);
    protected:
        void updateFPS(void);
        sf::Time lastFrameTime = sf::Time::Zero;
        std::vector<std::vector<int>> clicks = {};
        bool mouseWasDownLastFrame = false;
        bool mouseButtonState = false;
        sf::Mouse::Button mouseButtonPressed = sf::Mouse::Button::Left;

};

#include "ui/menu.hpp"

inline Engine::Engine() {
    window = new Window(width, height);
    clock = new sf::Clock;
}

inline Engine::Engine(int width, int height) {
    this->width = width;
    this->height = height;
    window = new Window(width, height);
    clock = new sf::Clock;
}

inline void Engine::run(void) {
    std::cout << "Running engine..." << std::endl;
    while (window->sfmlWindow->isOpen()) {
        // Main loop is run every frame
        // Update FPS
        updateFPS();
        // Update mouse
        mousePosition = sf::Mouse::getPosition(*(window->sfmlWindow));
        if (!mouseButtonState && mouseWasDownLastFrame) {
            int bp = this->mouseButtonPressed;
            this->clickAt(mousePosition.x, mousePosition.y, bp);
        }
        // Update state
        mouseWasDownLastFrame = mouseButtonState;
        // Clear the screen
        this->clearScreen();
        (*mainLoopFn)(this, window->sfmlWindow);
        // If the engine is not in a menu, run the game loop
        if (!inMenu) {
            (*gameLoopFn)(this, window->sfmlWindow);
        } else {
            // Run the active menu's cycle method
            (*activeMenu).cycle();
            // Draw the active menu's surface to the window
        }
        this->popClick();
        // Display
        window->sfmlWindow->display();
    }
}

inline void Engine::stop(void) {
    window->sfmlWindow->close();
}

inline void Engine::setMainLoop(void (*fn)(Engine *e, sf::RenderWindow *window)) {
    mainLoopFn = fn;
}

inline void Engine::setGameLoop(void (*fn)(Engine *e, sf::RenderWindow *window)) {
    gameLoopFn = fn;
}

inline void Engine::setEventHandler(void (*callback)(Engine *e, sf::Event event)) {
    eventHandler = callback;
}

inline void Engine::processEvents(void) {
    sf::Event event;
    while (window->sfmlWindow->pollEvent(event)) {
        (*eventHandler)(this, event);
    }
}

inline void Engine::clearScreen(void) {
    window->sfmlWindow->clear(clearColor);
}

inline void Engine::setClearColor(sf::Color c) {
    clearColor = c;
}

inline int Engine::addMenu(Menu *m) {
    this->menus.push_back(m);
    return this->menus.size() - 1;
}

inline void Engine::setMenu(int index) {
    if (index < 0 || index > this->menus.size()) {
        throw invalid_index_exception((char*)("index must be greater than 0 and less than the number of menus"));
    }
    this->activeMenu = this->menus[index];
}

inline void Engine::setMouseButtonState(bool s, sf::Mouse::Button b) {
    this->mouseButtonState = s;
    this->mouseButtonPressed = b;
}

inline void Engine::updateFPS(void) {
    sf::Time currentFrameTime = clock->getElapsedTime();
    deltaTime = (currentFrameTime - lastFrameTime).asMilliseconds();
    lastFrameTime = currentFrameTime;
    fps = 1000 / deltaTime;
}

inline int Engine::clickAt(int x, int y, int button) {
    this->clicks.push_back(std::vector<int> {x, y, button});
    return this->clicks.size() - 1;
}

inline std::vector<int> Engine::getClick(int index) {
    if (index < this->clicks.size() && index >= 0) {
        return this->clicks[index];
    }
    return std::vector<int> {-1, -1, -1};
}

inline void Engine::popClick(void) {
    if (this->clicks.size() > 0) {
        this->clicks.erase(this->clicks.begin());
    }
}