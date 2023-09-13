import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np

# Define the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Vertex shader source code
vertex_shader_code = """
#version 120
attribute vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Fragment shader source code for the Mandelbrot set
fragment_shader_code = """
#version 120
uniform vec2 resolution;
uniform int max_iterations;

void main()
{
    vec2 uv = (2.0 * gl_FragCoord.xy - resolution) / min(resolution.y, resolution.x);
    vec2 z = uv;
    int i;
    for (i = 0; i < max_iterations; i++)
    {
        if (length(z) > 2.0)
            break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + uv;
    }
    float color = float(i) / float(max_iterations);
    gl_FragColor = vec4(vec3(color), 1.0);
}
"""


def create_shader_program():
    # Create and compile the vertex shader
    vertex_shader = shaders.compileShader(vertex_shader_code, GL_VERTEX_SHADER)

    # Create and compile the fragment shader
    fragment_shader = shaders.compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)

    # Link the shaders into a shader program
    shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

    return shader_program


def main():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)

    shader_program = create_shader_program()
    glUseProgram(shader_program)

    resolution_uniform = glGetUniformLocation(shader_program, "resolution")
    max_iterations_uniform = glGetUniformLocation(shader_program, "max_iterations")

    glUniform2f(resolution_uniform, WINDOW_WIDTH, WINDOW_HEIGHT)
    glUniform1i(
        max_iterations_uniform, 1000
    )  # Adjust the maximum number of iterations as needed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        pygame.display.flip()


if __name__ == "__main__":
    main()
