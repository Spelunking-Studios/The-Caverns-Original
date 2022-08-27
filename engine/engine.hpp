#include <iostream>
#include <window.hpp>

class Engine {
    public:
        // Constructor & Destructor
        Engine();
        // Properties
        Window* window;
        // Methods
        void run(void);
};

inline Engine::Engine() {
    window = new Window();
}

inline void Engine::run(void) {
    std::cout << "Running engine..." << std::endl;
}