#pragma once

#include <vector>
#include <fstream>
#include <iostream>

#include <rapidjson/document.h>
#include <rapidjson/pointer.h>
#include <rapidjson/error/en.h>

#include "room.hpp"

using namespace rapidjson;

class Floor {
    public:
        Floor(int floorNumber);
        void load(void);
        void load(Document *doc);
    protected:
        int number;
        std::vector<Room<Floor>*> rooms = {};
};

inline Floor::Floor(int floorNumber) {
    this->number = floorNumber;
}

inline void Floor::load(void) {
    // Read floor data
    std::string fn = "assets/levelData/floorData.json";
    std::ifstream fdf;
    fdf.open(fn);
    if (!fdf.is_open()) {
        std::cerr << "Error: failed to open floor data file (" << strerror(errno) << ")." << std::endl;
        _Exit(1);
    }
    std::string data;
    while (fdf.good()) {
        std::string s;
        fdf >> s;
        data += s;
    }
    fdf.close();
    Document doc;
    if (doc.Parse(data.c_str()).HasParseError()) {
        std::cerr << "Error: encountered error while parsing floor data file." << std::endl;
        std::cerr << "\tJSON Error(offset " << (unsigned)doc.GetErrorOffset() <<
            "): " << GetParseError_En(doc.GetParseError()) << std::endl;
        _Exit(1);
    }
    // Find the data for this floor
    std::string dataPath = "/floors/";
    dataPath += std::to_string(this->number);
    dataPath += "/roomCount";
    Value *rd = Pointer(dataPath.c_str()).Get(doc);
    if (!rd || !rd->IsInt()) {
        std::cerr << "Error: malformed floor data." << std::endl;
        _Exit(1);
    }
    int numberOfRooms = rd->GetInt();
    for (int i = 0; i < numberOfRooms; i++) {
        this->rooms.push_back(
            new Room<Floor>(i)
        );
    }
    std::cout << "Floor " << number << " loaded with " << numberOfRooms << " rooms." << std::endl;
}

inline void Floor::load(Document *doc) {
    // Find the data for this floor
    std::string dataPath = "/floors/";
    dataPath += std::to_string(this->number);
    dataPath += "/roomCount";
    Value *rd = Pointer(dataPath.c_str()).Get(*doc);
    if (!rd || !rd->IsInt()) {
        std::cerr << "Error: malformed floor data." << std::endl;
        _Exit(1);
    }
    int numberOfRooms = rd->GetInt();
    std::cout << "Floor " << number << " loaded with " << numberOfRooms << " rooms." << std::endl;
}