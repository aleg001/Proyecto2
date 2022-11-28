# Desplegar resultado
# Referencia: https://www.geeksforgeeks.org/python-pil-image-show-method/
import time
from PIL import Image


from RayTracer import *
from Model import *


WhiteSpacial = Color(250, 252, 254)


grisito = Materiales(defuse=Color(237, 234, 234), albedo=[0.6, 0.3, 0], spec=35)
glossWhite = Materiales(defuse=Color(200, 200, 200), albedo=[1.3, 0.1, 0], spec=50)
glossRed = Materiales(defuse=Color(242, 68, 65), albedo=[1.3, 0.1, 0], spec=50)
# Color de naricita
orangeColor = Materiales(defuse=Color(255, 165, 0), albedo=[0.6, 0.3, 0], spec=35)
# Color de Naricita
Brown = Materiales(defuse=Color(139, 69, 19), albedo=[0.6, 0.3, 0], spec=35)
green = Materiales(defuse=Color(0, 255, 0), albedo=[0.6, 0.3, 0], spec=35)
red = Materiales(defuse=Color(255, 0, 0), albedo=[0.6, 0.3, 0], spec=35)
Black = Materiales(defuse=Color(0, 0, 0), albedo=[0.6, 0.3, 0], spec=35)


def Osito():
    return [
        # Pancita 1
        Sphere(V3(-4, 1, -15), 2.5, grisito),
        # Pancita 2
        Sphere(V3(4, 1, -15), 2.5, glossRed),
        # Piecito 1
        Sphere(V3(-6, 4, -15), 1, glossWhite),
        Sphere(V3(-3, 4, -15), 1, glossWhite),
        # Piecito 2
        Sphere(V3(6, 4, -15), 1, orangeColor),
        Sphere(V3(3, 4, -15), 1, orangeColor),
        # Bracito 1
        Sphere(V3(-7, -1, -15), 1, glossWhite),
        Sphere(V3(-1.5, -1, -15), 1, glossWhite),
        # Bracito 2
        Sphere(V3(7, -1, -15), 1, orangeColor),
        Sphere(V3(1.5, -1, -15), 1, orangeColor),
        # Detalle de pancita
        Sphere(V3(-4, 0, -15), 0.5, glossRed),
        Sphere(V3(4.5, 0, -15), 0.5, green),
        # Cabecita
        Sphere(V3(-4.2, -3, -15), 2.2, glossWhite),
        Sphere(V3(4.2, -3, -15), 2.2, orangeColor),
        # Orejitas
        Sphere(V3(-6, -5, -15), 0.5, glossWhite),
        Sphere(V3(-3, -5, -15), 0.5, glossWhite),
        Sphere(V3(6, -5, -15), 0.5, Brown),
        Sphere(V3(3, -5, -15), 0.5, Brown),
        # Naricita
        Sphere(V3(-4.2, -2.8, -15), 1.2, glossWhite),
        Sphere(V3(4.5, -2.8, -15), 1.2, Brown),
        # Detalle Naricita
        Sphere(V3(-4.2, -2.8, -15), 0.2, Black),
        Sphere(V3(4.5, -2.8, -15), 0.2, Black),
        # Ojitos
        Sphere(V3(-5.2, -4.3, -15), 0.4, Black),
        Sphere(V3(-3.5, -4.3, -15), 0.4, Black),
        Sphere(V3(5.5, -4.3, -15), 0.4, Black),
        Sphere(V3(3.5, -4.3, -15), 0.4, Black),
    ]


def run(filename):
    Raytracer = RayTracer(1000, 1000)
    Raytracer.clearColor = WhiteSpacial
    Raytracer.light = Luz(V3(-0, 0, 0), 1, Color(255, 255, 255))
    Raytracer.scene = Osito()
    Raytracer.Render()
    Raytracer.write(filename)
    im = Image.open(filename)
    im.show()
