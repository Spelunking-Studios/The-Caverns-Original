#version 330 core

uniform sampler2D tex;
uniform float time;

uniform vec3 effect_color = vec3(0.2, 0.3, 0.8);
uniform int octave_count = 10;
uniform float amp_start = 0.5;
uniform float amp_coeff = 0.5;
uniform float freq_coeff = 2.0;
uniform float speed = 0.5;
uniform float threshold = 0.2;

in vec2 uvs;
out vec4 f_color;

float hash12(vec2 x) {
    return fract(cos(mod(dot(x, vec2(13.9898, 8.141)), 3.14)) * 43758.5453);
}

vec2 hash22(vec2 uv) {
    uv = vec2(dot(uv, vec2(127.1,311.7)),
              dot(uv, vec2(269.5,183.3)));
    return 2.0 * fract(sin(uv) * 43758.5453123) - 1.0;
}

float noise(vec2 uv) {
    vec2 iuv = floor(uv);
    vec2 fuv = fract(uv);
    vec2 blur = smoothstep(0.0, 1.0, fuv);
    return mix(mix(dot(hash22(iuv + vec2(0.0,0.0)), fuv - vec2(0.0,0.0)),
                   dot(hash22(iuv + vec2(1.0,0.0)), fuv - vec2(1.0,0.0)), blur.x),
               mix(dot(hash22(iuv + vec2(0.0,1.0)), fuv - vec2(0.0,1.0)),
                   dot(hash22(iuv + vec2(1.0,1.0)), fuv - vec2(1.0,1.0)), blur.x), blur.y) + 0.5;
}

float fbm(vec2 uv, int octaves) {
    float value = 0.0;
    float amplitude = amp_start;
    for (int i = 0; i < octaves; i++) {
        value += amplitude * noise(uv);
        uv *= freq_coeff;
        amplitude *= amp_coeff;
    }
    return value;
}

vec3 checkDarkColor(vec3 color, vec3 texColor, float threshold) {
    float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722)); // Luminance
    return brightness < threshold ? texColor : color;
}
vec3 blendAdd(vec3 base, vec3 blend) {
    return base + blend;
}

void main() {
    vec2 uv = 2.0 * uvs - 1.0;
    uv += 2.0 * fbm(uv + time * speed, octave_count) - 1.0;
    float dist = abs(uv.y);
    vec3 color = effect_color * mix(0.0, 0.05, hash12(vec2(time))) / dist;

    // vec3 finalColor = checkDarkColor(color, texture(tex, uvs).rgb, threshold);
    vec3 finalColor = blendAdd(color, texture(tex, uvs).rgb);
    f_color = vec4(finalColor, 0.6);
}


