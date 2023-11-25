# nuevo lenguaje de porgramacion llamado GLSL
# Graphics Library Shaders Language

# Vertex shader to recreate texture.
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

# Fragment shader to recreate texture.
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

# Shader to recreate Gourad shading.
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

# --------------------------------- My Vertex Shaders ---------------------------------

# Shader to recreate waving effect.
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

# Shader to recreate breathing effect.
breathing_vertex_shader = """
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
    float radius = length(position.xz);
    float displacement = sin(time - radius * 2.0) * 0.1;
    vec3 newPosition = position + normalize(position) * displacement;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPosition, 1.0);
    UVs = texCoords;
    normal = normalize((modelMatrix * vec4(normals, 0.0)).xyz);
}
"""

# Shader to recreate glitch effect.
# The numbers 12.9898, 78.233, and 43758.5453123 are used in the pseudo-random number generator 
# to create a “seed” for generating random numbers. 
glitch_vertex_shader = """
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

float random (vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
    float glitchIntensity = 0.2;
    vec3 pos = position;
    pos.x += glitchIntensity * (random(vec2(time, position.y)) - 0.5);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
    normal = normalize((modelMatrix * vec4(normals, 0.0)).xyz);
}
"""

# --------------------------------- My Fragment Shaders ---------------------------------

# Shader to recreate Mario Star effect.
mariostar_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    vec3 norm = normalize(normal);
    vec3 color = vec3(1.0, 1.0, 1.0);
    vec3 normal2 = normalize(norm + color);
    float intensity = max(1.0, dot(normal2, -vec3(1.0, 1.0, 1.0)));
    fragColor = texture(tex, UVs) * vec4(normal2, 1.0) * intensity;
}
"""

# Shader to recreate glowing gold effect.
glowing_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform float time;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    vec3 norm = normalize(normal);
    vec3 color = vec3(cos(time/2.0 + 1.0), cos(time/2.0 + 2.0), cos(time/2.0 + 3.0));
    vec3 normal2 = normalize(norm + color);
    float intensity = abs(dot(normal2, vec3(1.0, 1.0, 1.0)));
    vec3 goldColor = vec3(1.0, 0.843, 0.0);
    fragColor = texture(tex, UVs) * vec4(goldColor, 0.5) * intensity;
}
"""

# Shader to recreate moving colors effect.
rainbow_fragment_shader = """
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform float time;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    vec3 norm = normalize(normal);
    vec3 color = vec3(1.0, 1.0, 1.0);
    vec3 normal2 = normalize(norm + color);
    float intensity = max(1.0, dot(normal2, -vec3(1.0, 1.0, 1.0)));
    vec3 movingColor = vec3((sin(time + normal.x) + 1.0) / 2.0, (sin(time + normal.y) + 1.0) / 2.0, (sin(time + normal.z) + 1.0) / 2.0);
    fragColor = texture(tex, UVs) * vec4(movingColor, 1.0) * intensity;
}
"""