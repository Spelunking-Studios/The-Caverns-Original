#version 330 core

uniform sampler2D tex;
uniform vec2 center;
uniform float size;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x, uvs.y);

    f_color = vec4(texture(tex, uvs).rgb * min(1, 1/(distance(uvs, center)*4)), 1.0 + size * 0.001);
}
