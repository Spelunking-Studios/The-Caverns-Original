#include "theCaverns.hpp"
#include "game.hpp"

using namespace rapidjson;

Game::Game(Engine *e) {
    this->e = e;
    // Create the game's surface
    this->surface = new Surface(0, 0, screenWidth, screenHeight);
    this->surface->setFillColor(sf::Color::Black);
    this->surface->fill();
    // Create the camera
    this->camera = new Camera(0, 0, screenWidth, screenHeight);
}

void Game::load(void) {
    // Read floor data
    std::string fn = "assets/levelData/floorData.json";
    std::ifstream fdf;
    fdf.open(fn);
    if (!fdf.is_open()) {
        std::cerr << "Error: failed to open floor data file (" << strerror(errno) << ")." << std::endl;
        e->stop();
        _Exit(1);
    }
    std::string data;
    while (fdf.good()) {
        std::string s;
        fdf >> s;
        data += s;
    }
    fdf >> data;
    fdf.close();
    Document doc;
    if (doc.Parse(data.c_str()).HasParseError()) {
        std::cerr << "Error: encountered error while parsing floor data file." << std::endl;
        std::cerr << "\tJSON Error(offset " << (unsigned)doc.GetErrorOffset() <<
            "): " << GetParseError_En(doc.GetParseError()) << std::endl;
        e->stop();
        _Exit(1);
    }
    // Find the data for this floor
    std::string dataPath = "/floorCount";
    Value *fdata = Pointer(dataPath.c_str()).Get(doc);
    if (!fdata) {
        std::cerr << "Error: malformed floor data." << std::endl;
        e->stop();
        _Exit(1);
    }
    int numberOfFloors = fdata->GetInt();
    std::cout << "Loaded game with " << numberOfFloors << " floors." << std::endl;
    // Create all of the floors
    for (int i = 0; i < numberOfFloors; i++) {
        this->floors.push_back(
            new Floor(i)
        );
    }
    // Load all of the floors
    for (int i = 0; i < this->floors.size(); i++) {
        this->floors[i]->load(&doc);
    }
    this->loaded = true;
}

void Game::cycle(sf::RenderWindow *window) {
    this->draw(window);
}

void Game::draw(sf::RenderWindow *window) {
    (*this->surface) >> (*window);
}