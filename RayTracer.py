from math import pi, tan
import math
import struct

from Model import *

from Model import Materiales


def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def doubleword(d):
    return struct.pack("=l", d)


class RayTracer(object):
    def __init__(self, w, h) -> None:
        self.w = w
        self.h = h
        self.scene = []
        self.clearColor = None
        self.currentColor = Color(255, 255, 255)
        self.light = None
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.clearColor for x in range(self.w)] for y in range(self.h)
        ]

    def point(self, x, y, color=None):
        if y >= 0 and y < self.h and x >= 0 and x < self.w:
            self.framebuffer[y][x] = color or self.currentColor

    def Render(self):
        fieldOfView = math.pi / 2
        fieldOfView = int(fieldOfView)
        ratio = self.w / self.h
        halfFieldOfView = fieldOfView / 2
        tanFieldOfView = tan(halfFieldOfView)

        for y in range(self.h):
            for x in range(self.w):
                tempOp = x + 0.5
                tempOp2 = y + 0.5
                i = (2 * (tempOp) / self.w - 1) * ratio * tanFieldOfView
                j = (1 - (2 * (tempOp2) / self.h)) * tanFieldOfView
                origen = V3(0, 0, 0)
                direccion = V3(i, j, -1).Normalizando()
                rayoCasteado = self.RayCasting(origen, direccion)
                self.point(x, y, rayoCasteado)

    def RayCasting(self, origen, direccion, r=0):
        if r == 3:
            return self.clearColor

        material, interseccion = self.interseccion1(origen, direccion)

        if material == None:
            return self.clearColor

        direccionLuz = (self.light.posicion - interseccion.point).Normalizando()

        ogSombra = interseccion.point + interseccion.normal * 1.1
        mSombra = self.interseccion1(ogSombra, direccionLuz)
        intSom = 0
        if mSombra:
            intSom = 0.3

        sombraIntensa = direccionLuz @ interseccion.normal

        dInt = material.defuse * sombraIntensa * material.albedo[0] * (1 - intSom)

        lReflex = Reflexiones(direccionLuz, interseccion.normal)
        reflejoIntensidad = max(0, (lReflex @ direccion))
        specularIntensidad = reflejoIntensidad**material.spec
        specular = self.light.color * specularIntensidad * material.albedo[1]
        if material.albedo[2] > 0:
            rDir = direccion * -1
            reflDir = Reflexiones(rDir, interseccion.normal)
            rOrigen = interseccion.point + interseccion.normal * 1.1
            rColor = self.RayCasting(rOrigen, reflDir, r + 1)
        else:
            rColor = Color(0, 0, 0)

        reflex = rColor * material.albedo[2]
        sumValue = dInt + specular + reflex

        return sumValue

    def interseccion1(self, origen, direcion):
        mat = None
        inters = None

        for i in self.scene:
            interseccion12 = i.intersectRay(origen, direcion)
            if interseccion12:
                if interseccion12.distance < 999999:
                    mat = i.material
                    inters = interseccion12
        return mat, inters

    def write(self, filename):
        w = self.w
        h = self.h
        f = open(filename, "wb")
        f.write(char("B"))
        f.write(char("M"))
        f.write(doubleword(14 + 40 + w * h * 3))
        f.write(doubleword(0))
        f.write(doubleword(14 + 40))
        f.write(doubleword(40))
        f.write(doubleword(w))
        f.write(doubleword(h))
        f.write(word(1))
        f.write(word(24))
        f.write(doubleword(0))
        f.write(doubleword(w * h * 3))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))

        for y in range(h):
            for x in range(w):
                f.write(self.framebuffer[y][x].toBytes())

        f.close()
