#pragma once

#include <exception>

class invalid_index_exception: public std::exception {
    public:
        invalid_index_exception(char* message) : message(message) {}
        char* what(void);
    protected:
        char* message;
};

inline char* invalid_index_exception::what(void) {
    char *ret = (char*)("Invalid index");
    return ret;
}