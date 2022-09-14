#pragma once

#include <iostream>
#include "../tiled/tiled.hpp"

template<class ParentT>
class Room {
    public:
        Room(int roomNumber);
        Room(int roomNumber, ParentT *p);
        int load(void);
        void setParent(ParentT *p);
    protected:
        int number;
        ParentT *parent;
        Map *map;
};

template<class ParentT>
inline Room<ParentT>::Room(int roomNumber) {
    this->number = roomNumber;
}

template<class ParentT>
inline Room<ParentT>::Room(int roomNumber, ParentT *p) {
    this->number = roomNumber;
    this->setParent(p);
}

template<class ParentT>
inline void Room<ParentT>::setParent(ParentT *p) {
    this->parent = p;
}

template<class ParentT>
inline int Room<ParentT>::load(void) {
    std::string tFilePath = "assets/Tiled/Floor";
    tFilePath += std::to_string(this->parent->getNumber() + 1);
    tFilePath += "/room";
    tFilePath += std::to_string(this->number + 1);
    tFilePath += ".json";
    // Map
    this->map = new Map(tFilePath);
    std::cout << "Room " << number + 1 << " of Floor " << parent->getNumber() + 1 << std::endl;
    return 0; // OK
}