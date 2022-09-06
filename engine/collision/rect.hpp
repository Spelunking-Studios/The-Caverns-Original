#pragma once

class RectCollider {
    public:
        RectCollider(int x, int y, int width, int height);
        bool pointCollide(int px, int py);
    protected:
        int x, y, width, height;
};

inline RectCollider::RectCollider(int x, int y, int width, int height) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
}

inline bool RectCollider::pointCollide(int px, int py) {
    return (px >= x && px <= (x + width) && py >= y && py <= (y + height));
}