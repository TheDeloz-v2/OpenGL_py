from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        self.scene = []
        self.clearColor = [0.0, 0.0, 0.0, 1.0]
        _, _, self.width, self.height = screen.get_rect()
        self.activeShader = None
        # View Matrix
        self.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
        self.cameraRotation = glm.vec3(0.0, 0.0, 0.0)
        self.viewMatrix = self.getViewMatrix()
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
        self.directionalLight = glm.vec3(0.0, -1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glViewport(0, 0, self.width, self.height)


    def updateViewMatrix(self):
        self.viewMatrix = self.getViewMatrix()
        
    
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

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(
                    glGetUniformLocation(self.activeShader, "modelMatrix"),
                    1,
                    GL_FALSE,
                    glm.value_ptr(obj.getModelMatrix())
                )
            obj.render()
            