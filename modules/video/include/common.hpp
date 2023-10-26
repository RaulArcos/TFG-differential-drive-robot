#ifndef COMMON_HPP_
#define COMMON_HPP_

struct Resolution{
    int width;
    int height;

    Resolution(
        int width = 0,
        int height = 0
    ):
        width(width),
        height(height)
    {};

    Resolution& operator=(const Resolution& other) {
        if (this != &other) {
            width = other.width;
            height = other.height;
        }
        return *this;
    }

};

#endif