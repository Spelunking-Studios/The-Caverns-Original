#pragma once

#include <string>
#include <fstream>
#include <iostream>
#include <vector>
#include <rapidjson/document.h>
#include <rapidjson/pointer.h>

#include "layer.hpp"

using namespace rapidjson;

class Map {
    public:
        Map(std::string fileName);
        float mapVersion, tiledVersion;
        int width, height;
        std::vector<Layer*> layers = {};
    protected:
        std::string fileName = "";
        Document *doc;
        Value* retriveFromDoc(std::string s);
};

inline Map::Map(std::string fileName) {
    this->fileName = fileName;
    // Read map file
    std::string mapString = "";
    std::ifstream mdf(fileName);
    if (!mdf.is_open()) {
        std::cerr << "Error: Failed to load map file (" << fileName << ")." << std::endl;
        _Exit(1);
    }
    while (mdf.good()) {
        std::string s;
        mdf >> s;
        mapString += s;
    }
    mdf.close();
    // Create the doc
    this->doc = new Document();
    doc->Parse(mapString.c_str());
    if (doc->HasParseError()) {
        std::cerr << "Error: Failed to parse map data (" << fileName << ")." << std::endl;
        std::cerr << "\tJSON Error(offset " << (unsigned)doc->GetErrorOffset() <<
            "): " << GetParseError_En(doc->GetParseError()) << std::endl;
        _Exit(1);
    }
    if (!doc->IsObject()) {
        std::cerr << "Error: invalid map data (root is not an object)." << std::endl;
        _Exit(1);
    }
    // Version
    Value *mvv = Pointer("/version").Get(*doc);
    if (!mvv || !(mvv->IsNumber() || mvv->IsString())) {
        std::cerr << "Error: Invalid, Undefined or Unrecognized map version." << std::endl;
        _Exit(1);
    }
    if (mvv->IsNumber()) {
        this->mapVersion = mvv->GetFloat();
    } else {
        this->mapVersion = std::stof(mvv->GetString());
    }
    // Tiled version
    Value *mtv = retriveFromDoc("/tiledversion");
    if (!mtv || !(mtv->IsNumber() || mtv->IsString())) {
        std::cerr << "Error: Invalid, Undefined or Unrecognized tiled version." << std::endl;
        _Exit(1);
    }
    if (mtv->IsNumber()) {
        this->tiledVersion = mtv->GetFloat();
    } else {
        this->tiledVersion = std::stof(mtv->GetString());
    }
    // Size (Width and Height)
    Value *wv = retriveFromDoc("/width");
    Value *hv = retriveFromDoc("/height");
    if (!wv || !wv->IsNumber()) {
        std::cerr << "Error: Invalid, Undefined or Unrecognized map width." << std::endl;
        _Exit(1);
    }
    if (!hv || !hv->IsNumber()) {
        std::cerr << "Error: Invalid, Undefined or Unrecognized map height." << std::endl;
        _Exit(1);
    }
    this->width = wv->GetInt();
    this->height = hv->GetInt();
    // Layers
    Value *lv = retriveFromDoc("/layers");
    if (!lv || !lv->IsArray()) {
        std::cerr << "Error: Invalid, Undefined or Unrecognized map layers." << std::endl;
        _Exit(1);
    }
    for (auto &item : lv->GetArray()) {
        layers.push_back(new Layer(&item));
    }
    std::cout << "Map (" << width << "x" << height << "x" << layers.size() << ") loaded with version "
        << this->mapVersion << " (tiled " << this->tiledVersion << ")." << std::endl;
}

inline Value* Map::retriveFromDoc(std::string s) {
    Pointer p(s.c_str());
    if (!p.IsValid()) {
        std::cerr << "Error: Invalid JSON pointer for string: " << s << std::endl;
        return (new Value);
    }
    return p.Get(*doc);
}