from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import pygame
import numpy

class Renderer(object):
    def __init__(self, screen, background_texture_path):
        self.screen = screen
        self.scene = []
        self.clearColor = [0.0, 0.0, 0.0, 1.0]
        _, _, self.width, self.height = screen.get_rect()
        self.activeShader = None
        # View Matrix
        self.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
        self.cameraRotation = glm.vec3(0.0, 0.0, 0.0)
        self.target = glm.vec3(0.0, 0.0, 0.0)
        # Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60.0),  # FOV
            self.width / self.height,  # Aspect Ratio
            0.1,  # Near Plane
            1000.0  # Far Plane
        )
        self.filledMode = True
        self.elapsedTime = 0.0
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.fatness = 0.0
        self.directionalLight = glm.vec3(1.0, 0.0, 0.0)
        self.lightIntensity = 1.0
        
        # Load background image using Pygame
        self.background_texture = self.load_texture(background_texture_path) 

        # Create a quad for the background
        self.background_quad = self.create_quad()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glViewport(0, 0, self.width, self.height)


    def updateViewMatrix(self):
        self.viewMatrix = glm.lookAt(
            self.cameraPosition,
            self.target,
            glm.vec3(0.0, 1.0, 0.0)
        )
    
    def load_texture(self, filename):
        texture_surface = pygame.image.load(filename)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width, height = texture_surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id
    
    def create_quad(self):
        vertices = [
            -10.0, -10.0, -10.0, 0.0, 0.0,
             10.0, -10.0, -10.0, 1.0, 0.0,
             10.0,  10.0, -10.0, 1.0, 1.0,
            -10.0,  10.0, -10.0, 0.0, 1.0,
        ]

        indices = [0, 1, 2, 2, 3, 0]

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertices, dtype=numpy.float32), GL_STATIC_DRAW)

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, numpy.array(indices, dtype=numpy.uint32), GL_STATIC_DRAW)

        # Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Texture attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        return vao

    def render_background(self):
        glUseProgram(self.activeShader)

        # Bind the background texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        glUniform1i(glGetUniformLocation(self.activeShader, "backgroundTexture"), 0)

        # Render the background quad
        glBindVertexArray(self.background_quad)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        # Unbind the texture
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def load_new_background(self, image_path):
        self.background_texture = self.load_texture(image_path)
    
    def toggleFilledMode(self):
        self.filledMode = not self.filledMode

        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT, GL_FILL)
        else:
            # glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    
    def getViewMatrix(self):
        identity = glm.mat4(1.0)

        translateMat = glm.translate(identity, self.cameraPosition)

        pitch = glm.rotate(identity, glm.radians(self.cameraRotation.x), glm.vec3(1.0, 0.0, 0.0))
        yaw = glm.rotate(identity, glm.radians(self.cameraRotation.y), glm.vec3(0.0, 1.0, 0.0))
        roll = glm.rotate(identity, glm.radians(self.cameraRotation.z), glm.vec3(0.0, 0.0, 1.0))

        rotationMat = pitch * yaw * roll

        camMatrix = translateMat * rotationMat

        return glm.inverse(camMatrix)
           

    def setShader(self, vertex_shader=None, fragment_shader=None):
        if vertex_shader is None and fragment_shader is None:
            self.activeShader = None
        else:
            self.activeShader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER))
            
            
    def render(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the background first
        self.render_background()

        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            # Set uniforms
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "viewMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.viewMatrix)
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "projectionMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.projectionMatrix)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "time"),
                self.elapsedTime
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "fatness"),
                self.fatness
            )
            glUniform3fv(
                glGetUniformLocation(self.activeShader, "directionalLight"),
                1,
                glm.value_ptr(self.directionalLight)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "lightIntensity"),
                self.lightIntensity
            )

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(
                    glGetUniformLocation(self.activeShader, "modelMatrix"),
                    1,
                    GL_FALSE,
                    glm.value_ptr(obj.getModelMatrix())
                )
            obj.render()
            