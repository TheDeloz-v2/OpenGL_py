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
