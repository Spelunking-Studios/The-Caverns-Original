#version 330 core

uniform sampler2D tex;
uniform float size;
uniform float spin;

uniform vec2 center;

in vec2 uvs;
out vec4 f_color;

vec2 rotate(vec2 point, vec2 center, float angle) {
    // Translate point to origin
    vec2 translated = point - center;
    
    // Create the rotation matrix
    mat2 rotation = mat2(
        cos(angle), -sin(angle),
        sin(angle),  cos(angle)
    );
    
    // Apply rotation and translate back
    return rotation * translated + center;
}

void main() {
    vec2 sample_pos = rotate(uvs, center, pow(3, -1 * pow(distance(uvs, center)*size, 2))*spin);

    f_color = vec4(texture(tex, sample_pos).r, texture(tex, sample_pos).g, texture(tex, sample_pos).b , 1.0);
}
