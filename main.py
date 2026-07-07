from rendering_algorithms import *
import pygame
from pygame.locals import *

def display():
    vertices = [[-3, -2, -3], [-3, -2, 3], [3, -2, -3], [3, -2, 3]]
    pygame.init()
    display = [640, 480]
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glFrustum(-0.011, 0.011, -0.0082, 0.0082, 0.02, 100)
    glTranslatef(0, 0, -10)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        generate_surface(vertices, 500, [4, 4, -2], 0.5)
        pygame.display.flip()
        pygame.time.wait(10)

display()