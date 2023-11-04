# nuevo lenguaje de porgramacion llamado GLSL
# Graphics Library Shaders Language

vertex_shader = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 normal;

void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
    normal = normalize(
        (modelMatrix * vec4(normals, 0.0)).xyz
    );
}
'''

fragment_shader = '''
 #version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    fragColor = texture(tex, UVs);
}
'''

gourad_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 directionalLight;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    float intensity = dot(normal, -directionalLight);
    fragColor = texture(tex, UVs) * intensity;
}
"""


# Shader to recreate rainbow colors, as time pases it change between red, orange, yellow, green, blue, indigo and violet.
rainbow_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform float time;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    float red = (sin(time) + 1.0) / 2.0;
    float green = (sin(time + 2.0) + 1.0) / 2.0;
    float blue = (sin(time + 4.0) + 1.0) / 2.0;
    fragColor = texture(tex, UVs) * vec4(red, green, blue, 1.0);
}
"""


waving_vertex_shader = """
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 normal;

void main() {
    float amplitude = 0.1;
    float frequency = 2.0;
    vec3 pos = position;
    pos.y += amplitude * sin(2.0 * 3.14159 * frequency * time + pos.x);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
    normal = normalize((modelMatrix * vec4(normals, 0.0)).xyz);
}
"""


shine_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform vec3 viewPos;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPos - norm);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 reflectDir = reflect(-lightDir, norm);
    vec3 viewDir = normalize(viewPos - norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 result = (0.2 + 0.8 * diff) * texture(tex, UVs).rgb + 0.5 * spec;
    fragColor = vec4(result, 1.0);
}
"""