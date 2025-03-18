#version 330 core

uniform sampler2D tex;
uniform float time;

uniform float exposure;
uniform float bloomStrength;

in vec2 uvs;
out vec4 f_color;

void main()
{
	vec3 sceneColor = texture(tex, uvs).rgb;
   
    // Apply a simple bloom effect by boosting bright areas
    vec3 bloomColor = max(sceneColor - vec3(0.8) + 0.001*time, 0.0) * bloomStrength;
    
    // Combine scene color with bloom effect
    vec3 finalColor = sceneColor + bloomColor;
    
    // Apply tone mapping (optional)
    finalColor = vec3(1.0) - exp(-finalColor * exposure);
    
    f_color = vec4(finalColor, 1.0);
}
