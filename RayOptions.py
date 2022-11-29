# Desplegar resultado
# Referencia: https://www.geeksforgeeks.org/python-pil-image-show-method/
import time
from PIL import Image


from RayTracer import *
from Model import *


WhiteSpacial = Color(250, 252, 254)

# Materiales (25 puntos):
VerdeGrama = Materiales(defuse=Color(0, 255, 0), albedo=[0.6, 0.3, 0.1, 0], spec=50)
AzulVolcan = Materiales(
    defuse=Color(0, 0, 101.98),
    albedo=[
        0.1,
        0.18725,
        0.1745,
        0.8,
    ],
    spec=0.297254,
)
Orquidea = Materiales(defuse=Color(255, 0, 255), albedo=[0.6, 0.3, 0.1, 0], spec=50)
RamasCafes = Materiales(defuse=Color(255, 255, 255), albedo=[0.6, 0.3, 0.1, 0], spec=50)
RojoRosas = Materiales(defuse=Color(255, 0, 0), albedo=[0.6, 0.3, 0.1, 0], spec=50)
BLUE = Materiales(defuse=Color(0, 0, 255), albedo=[0.6, 0.3, 0.1, 0], spec=20)
Purple = Materiales(defuse=Color(255, 0, 255), albedo=[0.6, 0.3, 0.1, 0], spec=50)
grisito = Materiales(defuse=Color(237, 234, 234), albedo=[0.6, 0.3, 0], spec=35)
glossWhite = Materiales(defuse=Color(200, 200, 200), albedo=[1.3, 0.1, 0], spec=50)
glossRed = Materiales(defuse=Color(242, 68, 65), albedo=[1.3, 0.1, 0], spec=50)
# Color de naricita
orangeColor = Materiales(defuse=Color(255, 165, 0), albedo=[0.6, 0.3, 0], spec=35)
# Color de Naricita
Brown = Materiales(defuse=Color(139, 69, 19), albedo=[0.6, 0.3, 0], spec=35)

BrownColor = Materiales(defuse=Color(139, 69, 19), albedo=[0.9, 0.1, 0.1, 0], spec=50)
green = Materiales(defuse=Color(0, 255, 0), albedo=[0.6, 0.3, 0], spec=35)
red = Materiales(defuse=Color(255, 0, 0), albedo=[0.6, 0.3, 0], spec=35)
Black = Materiales(defuse=Color(0, 0, 0), albedo=[0.6, 0.3, 0], spec=35)

DarkBlue = Materiales(defuse=Color(0, 0, 101.98), albedo=[0.6, 0.3, 0], spec=35)
""" 
   
""",


def Proyecto2():
    return [
        # Volcan
        Triangle(
            [
                V3(2 - 4, 1, -10),
                V3(4 - 4, -2, -10),
                V3(6 - 4, 1, -10),
                V3(2 - 4, 1, -10),
            ],
            BLUE,
        ),
        # Circulo de plantas
        Disco(V3(0, -2.9, -20), 9 + 3, 7.5 + 3, green),
        # Circulo de Madera
        Disco(V3(0, -2.9, -20), 8 + 3, 6.5 + 3, BrownColor),
        # Lago de ATITLAN
        Plane(V3(0, -1, -18), 15, 33, BLUE),
        # Grama de ATITLAN
        Plane(V3(0, -5, -20), 20, 25, VerdeGrama),
        # Representacion de petunias
        # Sphere(V3(3, 5, -15), 0.3, Purple),
        # Sphere(V3(4, 5, -15), 0.5, Purple),
        # Sphere(V3(-1, 5, -15), 0.4, Purple),
        # Sphere(V3(-1.5, 5, -15), 0.6, Purple),
        # Sphere(V3(0, 5, -15), 0.5, Purple),
        # Sphere(V3(2, 5, -15), 0.2, Purple),
        # Sphere(V3(3, 5 - 0.5, -15), 0.3, Purple),
        # Sphere(V3(4, 5 - 0.5, -15), 0.5, Purple),
        # Sphere(V3(-1, 5 - 0.5, -15), 0.4, Purple),
        # Sphere(V3(-1.5, 5 - 0.5, -15), 0.6, Purple),
        # Sphere(V3(0, 5 - 2.5, -15), 0.5, Purple),
        # Sphere(V3(2, 5 - 2.5, -15), 0.2, Purple),
        # Sphere(V3(3, 5 - 1.5, -15), 0.3, Purple),
        # Sphere(V3(4, 5 - 1.5, -15), 0.5, Purple),
        # Sphere(V3(-1 + 2, 5 - 1.5, -15), 0.4, Purple),
        # Sphere(V3(-1.5 + 2, 5 - 1.5, -15), 0.6, Purple),
        # Sphere(V3(0 + 1, 5 - 1.4, -15), 0.5, Purple),
        # Sphere(V3(2 + 2.1, 5 - 1.7, -15), 0.2, Purple),
        # Sphere(V3(1, 5, -15), 0.1, Purple),
        # Sphere(V3(2, 5, -15), 0.2, Purple),
        # Sphere(V3(-1, 5, -15), 0.1, Purple),
        # Sphere(V3(-1, 5.2, -15), 0.3, Purple),
        # Sphere(V3(0, 5.3, -15), 0.2, Purple),
        # Sphere(V3(2, 5.3, -15), 0.1, Purple),
        # Sphere(V3(3, 5.1 - 0.5, -15), 0.1, Purple),
        # Sphere(V3(4, 5.9 - 0.5, -15), 0.2, Purple),
        # Sphere(V3(-1, 4 - 0.5, -15), 0.2, Purple),
        # Sphere(V3(-1.5, 4 - 0.5, -15), 0.3, Purple),
        # Sphere(V3(0.1, 5 - 2.2, -15), 0.3, Purple),
        # Sphere(V3(2.2, 5 - 2.1, -15), 0.2, Purple),
        # Sphere(V3(3.3, 5 - 1.3, -15), 0.3, Purple),
        # Sphere(V3(4.5, 5 - 1.5, -15), 0.5, Purple),
        # Sphere(V3(-1.1 + 2, 5 - 1.5, -15), 0.4, Purple),
        # Sphere(V3(-1 + 2, 5 - 1.5, -15), 0.1, Purple),
        # Sphere(V3(0.1 + 1, 5 - 1.4, -15), 0.2, Purple),
        # Sphere(V3(2.01 + 2.1, 5 - 1.7, -15), 0.2, Purple),
    ]


def run(filename):
    Raytracer = RayTracer(1080, 1920)
    Raytracer.envmap = Envmap("bg.bmp")
    Raytracer.clearColor = WhiteSpacial
    Raytracer.light = Luz(V3(-0, 10, 0), 100, Color(255, 255, 255))
    Raytracer.scene = Proyecto2()
    Raytracer.Render()
    # Raytracer.glModel("gato.obj")
    Raytracer.write(filename)
    im = Image.open(filename)
    im.show()
