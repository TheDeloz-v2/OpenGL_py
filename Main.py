import pygame
from pygame.locals import *
from Renderer import Renderer
from Shaders import *
from Obj import Obj
import glm
import math

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen, "backgrounds/forest.jpg")
renderer.setShader(vertex_shader, fragment_shader)

isDragging = False

modelIndex = 0
musicIndex = 0
models = []
audio_files = ["music/pokemontheme.mp3", "music/tank.mp3", "music/zelda.mp3", "music/wii.mp3"]
sounds = [pygame.mixer.Sound(file) for file in audio_files]
sounds[musicIndex].play().set_volume(0.3)

def modelChange(direction):
    global modelIndex
    global models
    if direction == "R":
        if modelIndex == len(models) - 1:
            modelIndex = 0
        else:
            modelIndex += 1
            
    else:
        if modelIndex == 0:
            modelIndex = len(models) - 1
        else:
            modelIndex -= 1

    renderer.scene.clear()
    renderer.scene.append(models[modelIndex]['model'])
    renderer.lightIntensity = models[modelIndex]['lightIntensity']
    renderer.target = models[modelIndex]['lookAt']
    renderer.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
    renderer.directionalLight = models[modelIndex]['directionalLight']
    renderer.load_new_background(models[modelIndex]['backgroundImage'])
        
        
# Model 1: Mimikyu   
obj = Obj("models/mimikyu/mimikyu.obj", "models/mimikyu/mimikyu.png")
obj.model.position = glm.vec3(0.0, 0, -3.0)
obj.model.rotation = glm.vec3(0, 0, 0)
obj.model.scale = glm.vec3(0.5, 0.5, 0.5)
models.append({
    'model': obj.model,
    'lightIntensity': 1.0,
    'lookAt': glm.vec3(obj.model.position.x, obj.model.position.y, obj.model.position.z),
    'directionalLight': glm.vec3(0.0, -1.0, -1.0),
    'backgroundImage': "backgrounds/forest.jpg"
})

# Model 2: Tank
obj = Obj("models/tank/tank.obj", "models/tank/tank.png")
obj.model.position = glm.vec3(0.0, 0, -3.0)
obj.model.rotation = glm.vec3(0, 0, 0)
obj.model.scale = glm.vec3(0.3, 0.3, 0.3)
models.append({
    'model': obj.model,
    'lightIntensity': 1.0,
    'lookAt': glm.vec3(obj.model.position.x, obj.model.position.y, obj.model.position.z),
    'directionalLight': glm.vec3(0.0, -1.0, -1.0),
    'backgroundImage': "backgrounds/america.png"
})

# Model 3: Axe
obj = Obj("models/axe/axe.obj", "models/axe/axe.bmp")
obj.model.position = glm.vec3(0.0, 0, -2.0)
obj.model.rotation = glm.vec3(0, 0, 0)
obj.model.scale = glm.vec3(1, 1, 1)
models.append({
    'model': obj.model,
    'lightIntensity': 1.0,
    'lookAt': glm.vec3(obj.model.position.x, obj.model.position.y , obj.model.position.z),
    'directionalLight': glm.vec3(0.0, -1.0, -1.0),
    'backgroundImage': "backgrounds/pedestal.jpg"
})

# Model 4: Pin
obj = Obj("models/pin/pin.obj", "models/pin/pin.bmp")
obj.model.position = glm.vec3(0.0, 0, -2.0)
obj.model.rotation = glm.vec3(0, 0, 0)
obj.model.scale = glm.vec3(0.3, 0.3, 0.3)
models.append({
    'model': obj.model,
    'lightIntensity': 1.0,
    'lookAt': glm.vec3(obj.model.position.x, obj.model.position.y, obj.model.position.z),
    'directionalLight': glm.vec3(0.0, -1.0, -1.0),
    'backgroundImage': "backgrounds/telon.jpg"
})


renderer.scene.append(models[modelIndex]['model'])
renderer.lightIntensity = models[modelIndex]['lightIntensity']
renderer.target = models[modelIndex]['lookAt']
renderer.directionalLight = models[modelIndex]['directionalLight']

isRunning = True
sensibiilityZoom = 0.4
angle = 0.0
senX = 1
senY = 0.1

distance = abs(renderer.cameraPosition.z - models[modelIndex]['model'].position.z)
radius = distance

act_vertex_shader = vertex_shader
act_fragment_shader = fragment_shader

while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    
    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + models[modelIndex]['model'].position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + models[modelIndex]['model'].position.z

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_f:
                renderer.toggleFilledMode()
            if event.key == pygame.K_0:
                act_vertex_shader = vertex_shader
                act_fragment_shader = fragment_shader
            if event.key == pygame.K_1:
                act_fragment_shader = gourad_fragment_shader
            if event.key == pygame.K_2:
                act_fragment_shader = glowing_fragment_shader
            if event.key == pygame.K_3:
                act_fragment_shader = mariostar_fragment_shader
            if event.key == pygame.K_4:
                act_fragment_shader = rainbow_fragment_shader
            if event.key == pygame.K_5:
                act_fragment_shader = fragment_shader
            if event.key == pygame.K_6:
                act_vertex_shader = waving_vertex_shader
            if event.key == pygame.K_7:
                act_vertex_shader = glitch_vertex_shader
            if event.key == pygame.K_8:
                act_vertex_shader = breathing_vertex_shader
            if event.key == pygame.K_9:
                act_vertex_shader = vertex_shader
            
            if event.key == pygame.K_RIGHT:
                modelChange("R")
                if musicIndex+1 <= len(sounds):
                    sounds[musicIndex].stop()
                    musicIndex = (musicIndex + 1) % len(sounds)
                    sounds[musicIndex].play().set_volume(0.3)
                else:
                    sounds[musicIndex].stop()
                    musicIndex = 0
                    sounds[musicIndex].play().set_volume(0.3)
                angle = 0.0
                radius = distance    
            if event.key == pygame.K_LEFT:
                modelChange("L")
                if musicIndex != 0:
                    sounds[musicIndex].stop()
                    musicIndex = (musicIndex - 1) % len(sounds)
                    sounds[musicIndex].play().set_volume(0.3)
                else:
                    sounds[musicIndex].stop()
                    musicIndex = len(sounds) - 1
                    sounds[musicIndex].play().set_volume(0.3)
                angle = 0.0
                radius = distance
                
            renderer.setShader(act_vertex_shader, act_fragment_shader)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                isDragging = True
                oldPosition = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= sensibiilityZoom             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += sensibiilityZoom

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                isDragging = False

        elif event.type == pygame.MOUSEMOTION:
            if isDragging:
                newPosition = pygame.mouse.get_pos()
                deltax = newPosition[0] - oldPosition[0]
                deltay = newPosition[1] - oldPosition[1]
                angle += deltax * -senX

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -senY and distance * -1.5 < renderer.cameraPosition.y + deltay * -senY:
                    renderer.cameraPosition.y += deltay * -senY

                oldPosition = newPosition

    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()