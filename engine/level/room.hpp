#pragma once

#include <tinytmx.hpp>

template<class ParentT>
class Room {
    public:
        Room(int roomNumber);
        void setParent(ParentT *p);
    protected:
        int number;
        ParentT *parent;
};