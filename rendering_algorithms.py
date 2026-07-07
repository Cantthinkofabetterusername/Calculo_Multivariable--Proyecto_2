import sympy as sp
from OpenGL.GL import *

# La irradiancia se define como dΦ/dA, que es la radiancia incidente en
# una superficie. Como el área de una esfera es 4πr², podemos aproximar la
# irradiancia como:

def irradiance_aproximation(radiant_flux, point, light_source):
    distance_vector = sp.Matrix(light_source) - sp.Matrix(point)
    irradiance_aprox = radiant_flux / (4 * sp.pi * (distance_vector.norm())**2)
    return irradiance_aprox

# Se basa en la ecuación de renderizado para hacer el render del programa.
# Como la integral no se puede resolver de manera analítica, usamos el
# método de Monte Carlo para aproximar la integral:

def render(radiant_flux, point, light_source, BRDF, normal, number_of_samples):
    integral = 0
    Li = irradiance_aproximation(radiant_flux, point, light_source)
    samples = []

    for i in range(number_of_samples):
        theta = (i + 0.5) * (sp.pi / (2 * number_of_samples))
        phi = (i + 0.5) * (2 * sp.pi / number_of_samples)
        wi = sp.Matrix([
            sp.sin(theta) * sp.cos(phi),
            sp.cos(theta),               
            sp.sin(theta) * sp.sin(phi)
        ])
        samples.append(wi)

    for wi in samples:
        integral += BRDF * Li * max(0, normal.dot(wi))

    integral = (2 * sp.pi / number_of_samples) * integral
    return integral

# Función para obtener la normal:

def normal(surface):
    A = sp.Matrix(surface[0])
    B = sp.Matrix(surface[1])
    C = sp.Matrix(surface[2])
    AB = B - A
    AC = C - A
    normal = AB.cross(AC)
    normal = normal.normalized()
    return normal

# Usamos OpenGL y algoritmos geométricos para generar la superficie:

def generate_triangle(vertices, radiant_flux, light_source, reflection_percentage):
    normal_vector = normal(vertices)
    glBegin(GL_TRIANGLES)
    for vertice in vertices:
        Lo = render(radiant_flux, sp.Matrix(vertice), light_source, reflection_percentage / sp.pi, normal_vector, 10)
        glColor3f(Lo, Lo, Lo)
        glVertex3fv(vertice)
    glEnd()

def generate_surface(vertices, radiant_flux, light_source, reflection_percentage):
    triangle_vertices = [vertices[0], vertices[1], vertices[2]]
    generate_triangle(triangle_vertices, radiant_flux, light_source, reflection_percentage)
    triangle_vertices = [vertices[2], vertices[1], vertices[3]]
    generate_triangle(triangle_vertices, radiant_flux, light_source, reflection_percentage)