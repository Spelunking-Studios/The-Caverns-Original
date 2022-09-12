#pragma once

#include <string>
#include <tinytmx.hpp>

class Map {
    public:
        Map(std::string fileName);
    protected:
        std::string fileName = "";
};

inline Map::Map(std::string fileName) {
    this->fileName = fileName;
}