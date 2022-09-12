#pragma once

#include "surface.hpp"

class Camera {
    public:
        Camera(int x, int y, int width, int height);
        void moveTo(int x, int y);
        void resize(int width, int height);
        Surface* apply(Surface *s);
    protected:
        unsigned char signature = 0x0;
        int x, y, width, height;
        void sign(void);
};

inline Camera::Camera(int x, int y, int width, int height) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->sign();
}

inline void Camera::sign(void) {
    this->signature = 0x7;
}

inline void Camera::moveTo(int x, int y) {
    this->x = x;
    this->y = y;
}

inline void Camera::resize(int width, int height) {
    this->width = width;
    this->height = height;
}

inline Surface* Camera::apply(Surface *s) {
    Surface *r = new Surface(0, 0, width, height);
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            sf::Color c = s->getPixel(x + i, y + j);
            r->setPixel(i, j, c);
        }
    }
    return r;
}