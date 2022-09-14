#pragma once

#include <rapidjson/document.h>
#include <rapidjson/pointer.h>

using namespace rapidjson;

enum LayerType {
    IMAGE_LAYER,
    OBJECT_LAYER
}

class Layer {
    public:
        Layer(GenericValue<UTF8<> > *v);
    private:
        int type = -1;
};

inline Layer::Layer(GenericValue<UTF8<> > *v) {
    // Get the type
    if (v["type"] == "imageLayer") {
        type = LayerType::IMAGELAYER;
    } else if (v["type"] == "objectLayer") {
        type = LayerType::OBJECT_LAYER;
    } else {
        std::cerr << "Error: Unrecognized layer type: " << v["type"] << std::endl;
        _Exit(1);
    }
}