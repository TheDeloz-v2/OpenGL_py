import pygame
from pygame.locals import *
from Renderer import Renderer
from Model import Model
from Shaders import *
from Obj import Obj
import glm


width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

#Model loading
obj = Obj("model/modelsus.obj")
objData = []

for face in obj.faces:
    if len(face) == 3:
        for vertexInfo in face:
            vertexId, texcoordId, normalId = vertexInfo
            vertex = obj.vertices[vertexId - 1]
            normals = obj.normals[normalId - 1]
            uv = obj.texcoords[texcoordId - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
    elif len(face) == 4:
        for i in [0, 1, 2]:
            vertexInfo = face[i]
            vertexId, texcoordId, normalId = vertexInfo
            vertex = obj.vertices[vertexId - 1]
            normals = obj.normals[normalId - 1]
            uv = obj.texcoords[texcoordId - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
        for i in [0, 2, 3]:
            vertexInfo = face[i]
            vertexId, texcoordId, normalId = vertexInfo
            vertex = obj.vertices[vertexId - 1]
            normals = obj.normals[normalId - 1]
            uv = obj.texcoords[texcoordId - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)

print('Se cargo el modelo.')

# Texture loading
model = Model(objData)
model.loadTexture("model/modelsus.bmp")
model.position.x = 0
model.position.z = -12
model.position.y = -5
model.rotation.x = 0
model.rotation.z = 0
model.rotation.y = 0
model.scale = glm.vec3(0.05, 0.05, 0.05)
renderer.scene.append(model)
print('Se cargo la textura.')

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()