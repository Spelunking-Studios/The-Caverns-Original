#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 5 + time * 0.05) * 0.1, uvs.y);
    f_color = vec4(texture(tex, sample_pos).r, texture(tex, sample_pos).g, texture(tex, sample_pos).b , 1.0);
}
